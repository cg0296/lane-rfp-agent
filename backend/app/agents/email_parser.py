import json
from anthropic import Anthropic
from typing import Optional
from app.models import ParsedQuoteData
from app.config import settings


client = Anthropic()


PARSE_PROMPT = """You are an expert at parsing freight quote request emails. Extract the following information from the email:

Required:
- Origin city and state
- Destination city and state
- Equipment type (e.g., 53' trailer, flatbed, refrigerated, etc.)
- Quantity of trucks/loads

Optional:
- Driver type (solo, team, owner-op, etc.)
- Loading date or date range
- Delivery date
- Special requirements (insurance, e-track, commodity type, equipment specs, hazmat, etc.)

Return ONLY valid JSON (no markdown, no backticks) with this structure:
{{
  "origin_city": "string",
  "origin_state": "string (2-letter code)",
  "destination_city": "string",
  "destination_state": "string (2-letter code)",
  "equipment_type": "string",
  "driver_type": "string or null",
  "quantity": number,
  "loading_date_start": "YYYY-MM-DD or null",
  "loading_date_end": "YYYY-MM-DD or null",
  "delivery_date": "YYYY-MM-DD or null",
  "special_requirements": ["array of strings"],
  "confidence": 0.95,
  "notes": "any clarifications or missing info"
}}

Email to parse:
{email_text}"""


def parse_email(email_text: str, client_name: Optional[str] = None) -> ParsedQuoteData:
    """
    Parse a freight quote request email using Claude API.

    Args:
        email_text: The raw email content
        client_name: Optional client name from context

    Returns:
        ParsedQuoteData with extracted information

    Raises:
        ValueError: If parsing fails or JSON is invalid
    """

    prompt = PARSE_PROMPT.format(email_text=email_text)

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the response text
    response_text = message.content[0].text.strip()

    # Remove markdown code blocks if present
    if response_text.startswith("```json"):
        response_text = response_text[7:]  # Remove ```json
    if response_text.startswith("```"):
        response_text = response_text[3:]  # Remove ```
    if response_text.endswith("```"):
        response_text = response_text[:-3]  # Remove trailing ```

    response_text = response_text.strip()

    # Parse JSON
    try:
        parsed_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Claude's response as JSON: {e}\nResponse: {response_text}")

    # Validate required fields
    required_fields = [
        "origin_city", "origin_state", "destination_city", "destination_state",
        "equipment_type", "quantity"
    ]

    missing = [f for f in required_fields if f not in parsed_data or parsed_data[f] is None]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    # Convert to ParsedQuoteData model (validates types)
    return ParsedQuoteData(**parsed_data)


def improve_parse_with_user_feedback(
    original_parse: ParsedQuoteData,
    user_edits: dict,
    original_email: str
) -> ParsedQuoteData:
    """
    Re-parse email with user feedback to improve accuracy.

    Args:
        original_parse: The original parsed data
        user_edits: Fields the user corrected
        original_email: The original email text

    Returns:
        Updated ParsedQuoteData
    """

    # Convert original to dict and apply edits
    parse_dict = original_parse.model_dump()
    parse_dict.update(user_edits)

    # Return updated model
    return ParsedQuoteData(**parse_dict)

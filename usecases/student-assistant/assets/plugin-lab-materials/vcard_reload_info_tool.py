from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
import json
import re


@tool(
    name="vcard_reload_info",
    description="Provides information about reloading VCard Arlington Bucks through the secure VCash portal.",
    permission=ToolPermission.ADMIN
)
def vcard_reload_info(vcard_number: str, credit_card_last_four: str = None) -> str:
    """
    Provides VCard reload information and secure portal access details.
    
    This tool does NOT process actual financial transactions. It provides information
    about how students can securely reload their VCard Arlington Bucks through the
    official VCash portal at https://card.vassar.edu
    
    :param vcard_number: The VCard number (format: 999XXXXXX)
    :param credit_card_last_four: Last 4 digits of credit card if provided (optional)
    :return: Information about secure reload process as JSON string
    """
    # Validate VCard number format (must be 9 digits starting with 999)
    if not vcard_number or not re.match(r'^999\d{6}$', vcard_number):
        return json.dumps({
            "error": "Invalid VCard number format. VCard numbers should be 9 digits starting with 999 (e.g., 999123456)"
        })
    
    # Check if provided card matches the example linked card
    card_already_linked = False
    card_status_message = "You can link a new payment method through the secure portal."
    
    if credit_card_last_four:
        # Remove any non-digit characters
        last_four = re.sub(r'\D', '', credit_card_last_four)
        if last_four == "9876":
            card_already_linked = True
            card_status_message = "The card ending in 9876 appears to be already linked to your VCard account. You can use this card or add a new one through the portal."
    
    # Prepare the response with portal information
    result = {
        "status": "info_provided",
        "vcard_number": vcard_number,
        "portal_url": "https://card.vassar.edu",
        "portal_name": "VCash Login Portal",
        "message": "For your security, VCard reloads must be completed through the secure VCash portal. We cannot process credit card information through chat.",
        "portal_features": [
            "Make deposits to add Arlington Bucks",
            "Check your current VCard balance",
            "Report a lost or stolen card",
            "View your transaction history",
            "Manage linked payment methods"
        ],
        "card_status": card_status_message,
        "security_note": "Never share full credit card details in chat. Our system automatically redacts credit card numbers for your protection.",
        "next_steps": [
            "Visit https://card.vassar.edu",
            "Log in with your Vassar credentials",
            "Select 'Make a Deposit' to reload your Arlington Bucks",
            "Use your linked payment method or add a new one securely"
        ]
    }
    
    return json.dumps(result, indent=2)


# Created for Vassar College Student Assistant - VCard Services

# Made with Bob

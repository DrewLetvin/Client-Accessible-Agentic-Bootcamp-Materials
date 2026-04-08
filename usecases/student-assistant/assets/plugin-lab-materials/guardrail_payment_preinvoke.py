import re
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.tools.types import PythonToolKind, PluginContext, AgentPreInvokePayload, AgentPreInvokeResult


@tool(
    description="Pre-invoke plugin that redacts credit card numbers while preserving VCard numbers (999XXXXXX format).",
    kind=PythonToolKind.AGENTPREINVOKE
)
def guardrail_payment_preinvoke(plugin_context: PluginContext, agent_pre_invoke_payload: AgentPreInvokePayload) -> AgentPreInvokeResult:
    """
    Redacts credit card numbers in user messages while preserving VCard numbers.
    
    This plugin protects sensitive payment information (PII) while allowing
    institutional identifiers (VCard numbers) to remain visible.
    
    Examples:
    - Credit Card: 4532 1234 5678 9012 → **** **** **** 9012
    - Credit Card: 4532-1234-5678-9012 → **** **** **** 9012
    - Credit Card: 4532123456789012 → **** **** **** 9012
    - VCard: 999123456 → 999123456 (preserved - institutional ID, not PII)
    """
    
    user_input = ''
    modified_payload = agent_pre_invoke_payload
    res = AgentPreInvokeResult()
    
    # Extract user input from the payload
    if agent_pre_invoke_payload and agent_pre_invoke_payload.messages:
        user_input = agent_pre_invoke_payload.messages[-1].content.text
    
    def redact_credit_cards(text: str) -> str:
        """
        Redacts credit card numbers (16 digits) while preserving VCard numbers (999XXXXXX).
        
        Handles multiple credit card formats:
        - With spaces: 1234 5678 9012 3456
        - With dashes: 1234-5678-9012-3456
        - No separator: 1234567890123456
        
        VCard numbers (999XXXXXX) are explicitly preserved as they are institutional
        identifiers, not personally identifiable payment information.
        
        Args:
            text (str): The input text containing potential credit card numbers.
        
        Returns:
            str: The text with credit card numbers redacted, VCard numbers preserved.
        """
        # Pattern for credit cards (16 digits with optional spaces/dashes)
        # Uses negative lookahead (?!999\d{6}\b) to exclude VCard numbers
        # This ensures VCard numbers like 999123456 are NOT matched
        pattern = r'(?!999\d{6}\b)(\d{4})[\s-]?(\d{4})[\s-]?(\d{4})[\s-]?(\d{4})'
        
        # Replace with asterisks, keeping only the last 4 digits visible
        # \4 refers to the 4th capture group (last 4 digits)
        redacted = re.sub(pattern, r'**** **** **** \4', text)
        
        return redacted
    
    # Redact credit cards in the user input
    modified_text = redact_credit_cards(user_input)
    
    # Update the payload with redacted text
    modified_payload.messages[-1].content.text = modified_text
    res.modified_payload = modified_payload
    res.continue_processing = True
    
    return res


# Created for Vassar College Student Assistant - Payment Security Guardrail

# Made with Bob

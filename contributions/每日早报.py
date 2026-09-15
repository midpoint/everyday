import re
from datetime import date
from typing import Dict, Any, List

class DailyReportProcessor:
    """
    Analyzes and standardizes raw daily morning report text inputs 
    into a consistent, predictable data structure (JSON/Dict).
    """
    
    def __init__(self):
        # Define standard schema keys for normalization
        self.SCHEMA_KEYS = ["report_date", "source_type", "headline", "summary", "detail"]

    def _cleanse_text(self, text: str) -> str:
        """Strips common boilerplate/noise characters and excessive whitespace."""
        # Remove promotional or non-content phrases aggressively
        text = re.sub(r'欢迎大家来到.*|请联系微信\S+', '', text).strip()
        # Normalize multiple spaces/newlines
        return re.sub(r'\s+', ' ', text).strip()

    def parse_product_launch(self, raw_content: str) -> Dict[str, Any]:
        """Handles product launch formatted reports (Source 1)."""
        report = {"source_type": "Product Launch", "detail": [], "summary": None}
        
        # Regex pattern to capture the main announcement structure
        product_pattern = re.compile(r'([^\.]+\.)\s*(.*?)\.', re.DOTALL)
        matches = product_pattern.findall(raw_content)

        if matches:
            report['summary'] = "Multiple new product announcements detected."
            for match in matches:
                # Assuming the structure is [Brand/Theme] + Product Details
                theme = match[0].strip()
                details = match[1].strip()
                product_info = {
                    "brand": theme,
                    "headline": details.split("上新")[0].replace('-', '').strip(),
                    "product": details.split("上新")[-1].strip().rstrip('.'),
                    "description": details
                }
                report['detail'].append(product_info)
        else:
             report['summary'] = "Product pattern not found."

        return report


    def parse_global_news(self, raw_content: str) -> Dict[str, Any]:
        """Handles structured global news reports (Source 2)."""
        # Attempt to extract date/time metadata first
        date_match = re.search(r'(\d{4}-\d{1,2}-\d{1,2})', raw_content)
        report = {"source_type": "Global News Feed", "detail": [], "summary": ""}

        if date_match:
            report['report_date'] = date_match.group(1)
        else:
            report['report_date'] = str(date.today()) # Fallback

        # Regex targeting structured news blocks (assuming format like 'Topic: Content...')
        news_blocks = re.findall(r'([\w\s]+):\s*(.*?)(?=\n[\w\s]+\s*:|\Z)', raw_content, re.DOTALL)
        
        for topic, content in news_blocks:
            summary = self._cleanse_text(content).replace('\n', ' ')
            report['detail'].append({
                "topic": topic.strip(),
                "headline": summary[:70].strip() + "...",
                "summary": summary
            })
        
        return report


    def generate_daily_report(self, raw_input: str, source_tag: str = None) -> Dict[str, Any]:
        """Main dispatch function to route and process the input based on expected schema."""
        raw_cleaned = self._cleanse_text(raw_input)
        final_report = {
            "source_type": "Unknown", 
            "timestamp_processed": str(date.today()),
            "content": {}
        }

        if source_tag == "PRODUCT":
            final_report['content'] = self.parse_product_launch(raw_cleaned)
        elif source_tag == "NEWS":
            final_report['content'] = self.parse_global_news(raw_cleaned)
        else: # Default/Generic fallthrough (e.g., Source 3 type content)
             # Fallback for simple text blocks where only general summary is needed
            final_report['content'] = {
                "source_type": "General Update",
                "summary": raw_cleaned[:200] + "..." if len(raw_cleaned) > 200 else raw_cleaned,
                "detail": []
            }
        
        return final_report

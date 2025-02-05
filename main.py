import json
import sys
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access the API key
api_key = os.getenv('OPENAI_API_KEY')

def get_insurance_comparison(insurance_names):
    """
    Uses GPT-3.5-Turbo to research and compare insurance plans.
    """
    client = OpenAI(api_key=api_key)
    
    prompt = f"""Compare these insurance plans: {', '.join(insurance_names)}

    Analyze and provide:
    1. Total hospital cover
    2. CSR (Claim Settlement Ratio) rate
    3. Pros
    4. Cons
    5. Key features
    6. User Experience & Reviews
    7. Market Reputation
    8. Claim Processing Time
    9. Network Hospitals
    10. Additional Benefits
    
    Also include:
    - A detailed comparison between the plans
    - Common user complaints and praises
    - Market sentiment and trust factor
    - Digital experience (app/website usability)
    - Customer service quality
    - A recommendation for which plan is better and why
    - Three relevant Reddit discussions/reviews (with r/insurance or similar subreddit links)
    
    Format the response as a JSON object with this structure:
    {{
        "insurance_plans": {{
            "plan_name": {{
                "total_hospital_cover": number,
                "csr_rate": number,
                "claim_processing_time": "average time in days",
                "network_hospitals": number,
                "pros": [list of strings],
                "cons": [list of strings],
                "key_features": [list of strings],
                "user_experience": {{
                    "common_praises": [list of strings],
                    "common_complaints": [list of strings],
                    "app_rating": number,
                    "customer_service_rating": number
                }},
                "market_analysis": {{
                    "market_reputation": string,
                    "trust_score": number,
                    "market_share": string,
                    "trending_direction": "increasing/decreasing/stable"
                }},
                "additional_benefits": [list of strings],
                "reddit_reviews": [
                    {{
                        "title": "title of reddit post",
                        "summary": "brief summary of the discussion",
                        "link": "reddit.com link to the post",
                        "sentiment": "positive/negative/neutral",
                        "key_points": [list of main points from discussion]
                    }}
                ]
            }}
        }},
        "comparison": "detailed comparison text",
        "market_insights": {{
            "current_trends": [list of strings],
            "value_for_money": string
        }},
        "recommendation": {{
            "recommended_plan": "name of recommended plan",
            "reason": "explanation for recommendation",
            "best_suited_for": [list of strings]
        }}
    }}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert insurance analyst with deep knowledge of user experiences, market trends, and insurance products. Provide detailed, accurate information about insurance plans in JSON format, incorporating both technical details and real-world user feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000  # Increased token limit for more detailed response
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"Error getting insurance comparison: {str(e)}"}

if __name__ == "__main__":
    # Ensure OpenAI API key is set
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)
    
    # Get insurance names from command line arguments
    if len(sys.argv) < 3:
        print("Usage: python main.py <insurance1_name> <insurance2_name>")
        sys.exit(1)
        
    insurance_names = sys.argv[1:3]
    result = get_insurance_comparison(insurance_names)
    print(json.dumps(result, indent=4))

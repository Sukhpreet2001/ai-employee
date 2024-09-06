import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def process_user_query(query):
    tokens = word_tokenize(query.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    return filtered_tokens

def interpret_query(tokens):
    if "analyze" in tokens:
        return "analysis"
    elif "report" in tokens:
        return "generate_report"
    elif "upload" in tokens:
        return "upload_file"
    else:
        return "unknown"

# Example Usage
if __name__ == "__main__":
    query = input("Enter your query: ")
    tokens = process_user_query(query)
    action = interpret_query(tokens)
    print(f"User action: {action}")

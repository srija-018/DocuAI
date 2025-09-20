from Summarizer.models import ContentModel

class DBContentHandler:
    # Utility class to fetch and combine all content from the database
    @staticmethod
    def fetch_content():
        print("Fetching content from DB...")  
        contents = ContentModel.objects.all()

        if not contents.exists():
            print("No DB content found.")
            return "No content found in the database."

        combined = "\n\n".join(f"{obj.title}:\n{obj.content}" for obj in contents)
        print("DB content fetched successfully.")
        return combined

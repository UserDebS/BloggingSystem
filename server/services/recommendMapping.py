import numpy as np
from .dataCorrection import DataCorrection

def recommendMapping(boolList : list[bool], _type : str = 'dict') -> dict[str, bool] | list[str]:
    selected_topics : list[str] = np.array([
        "Technology", "Programming", "Web Development", "Data Science", "Machine Learning",
        "Artificial Intelligence", "Cybersecurity", "Gadgets & Reviews", "Software Development",
        "Cloud Computing", "Digital Marketing", "SEO", "Social Media", "Business & Entrepreneurship",
        "Finance & Investment", "Personal Finance", "Economics", "Career Development", "Productivity",
        "Lifestyle", "Health & Wellness", "Fitness", "Nutrition", "Travel", "Food & Recipes",
        "Cooking", "Home & Garden", "DIY & Crafts", "Parenting", "Education", "Books & Literature",
        "Art & Design", "Music", "Movies & TV Shows", "Gaming", "Photography", "Sports", "Automotive",
        "Real Estate", "Law & Legal", "Science", "History", "Politics", "Religion & Spirituality",
        "Philosophy", "Current Events", "Opinion & Commentary", "Humor", "Personal Stories",
        "Interviews", "How-To Guides", "Tutorials", "Reviews", "Case Studies", "Thought Leadership",
        "Guest Posts", "Product Announcements", "Tech News", "Event Coverage", "Trends & Innovations", "Relationship", "Advice", "Reading", "ReactJS"
    ])[boolList]
    if(_type == 'list'):
        return selected_topics
    return {DataCorrection(i) : True for i in selected_topics}


if __name__ == '__main__':
    print(recommendMapping([True if i % 2 == 0 else False for i in range(63)]))
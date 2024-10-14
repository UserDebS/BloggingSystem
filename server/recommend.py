from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import numpy as np

class Recommend:
    def __init__(self) -> None:
        self.nlp = spacy.load('en_core_web_md')
        self.__vectorizer = TfidfVectorizer(stop_words = 'english')
        self.__blog_topics = list(map(lambda x: x.vector, list(map(self.nlp, [
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
        ]))))

        self.__blog_topics_tfid = self.__vectorizer.fit_transform(["Technology", "Programming", "Web Development", "Data Science", "Machine Learning", "Artificial Intelligence", "Cybersecurity", "Gadgets & Reviews", "Software Development", "Cloud Computing", "Digital Marketing", "SEO", "Social Media", "Business & Entrepreneurship",
            "Finance & Investment", "Personal Finance", "Economics", "Career Development", "Productivity",
            "Lifestyle", "Health & Wellness", "Fitness", "Nutrition", "Travel", "Food & Recipes",
            "Cooking", "Home & Garden", "DIY & Crafts", "Parenting", "Education", "Books & Literature",
            "Art & Design", "Music", "Movies & TV Shows", "Gaming", "Photography", "Sports", "Automotive",
            "Real Estate", "Law & Legal", "Science", "History", "Politics", "Religion & Spirituality",
            "Philosophy", "Current Events", "Opinion & Commentary", "Humor", "Personal Stories",
            "Interviews", "How-To Guides", "Tutorials", "Reviews", "Case Studies", "Thought Leadership",
            "Guest Posts", "Product Announcements", "Tech News", "Event Coverage", "Trends & Innovations", "Relationship", "Advice", "Reading", "ReactJS"])

    def __threshold(self, val : float, threshold: float = 0.58) -> bool:
        return val >= threshold

    def compareHashTags(self, tags : list[str]) -> list[bool]:
        result = [False for i in range(len(self.__blog_topics))]
        for tag in tags:
            result = self.compareBoolList(result, self.compareHashTag(tag=tag))
        return result

    def compareHashTag(self, tag : str) -> list[bool]:
        return [self.__compareTo(tag, vecItem) for vecItem in self.__blog_topics]
    
    def compareBoolList(self, list1 : list[bool], list2 : list[bool]) -> list[bool]:
        return np.logical_or(list1, list2)
    
    def compareContent(self, content : str) -> list[bool]:
        return list(map(self.__threshold, cosine_similarity(self.__vectorizer.transform([content]), self.__blog_topics_tfid)[0]))

    def __compareTo(self, w1 : str, vec) -> bool:
        vector = self.nlp(w1).vector
        return self.__threshold(cosine_similarity([vector], [vec])[0][0])

if __name__ == '__main__':
    r = Recommend()
    print(np.array(["Technology", "Programming", "Web Development", "Data Science", "Machine Learning", "Artificial Intelligence", "Cybersecurity", "Gadgets & Reviews", "Software Development", "Cloud Computing", "Digital Marketing", "SEO", "Social Media", "Business & Entrepreneurship",
            "Finance & Investment", "Personal Finance", "Economics", "Career Development", "Productivity",
            "Lifestyle", "Health & Wellness", "Fitness", "Nutrition", "Travel", "Food & Recipes",
            "Cooking", "Home & Garden", "DIY & Crafts", "Parenting", "Education", "Books & Literature",
            "Art & Design", "Music", "Movies & TV Shows", "Gaming", "Photography", "Sports", "Automotive",
            "Real Estate", "Law & Legal", "Science", "History", "Politics", "Religion & Spirituality",
            "Philosophy", "Current Events", "Opinion & Commentary", "Humor", "Personal Stories",
            "Interviews", "How-To Guides", "Tutorials", "Reviews", "Case Studies", "Thought Leadership",
            "Guest Posts", "Product Announcements", "Tech News", "Event Coverage", "Trends & Innovations", "Relationship", "Advice", "Reading"])[r.compareContent('I love making food')])
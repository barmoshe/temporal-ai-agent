"""
JSON Array Creation Tool

This module provides a tool for creating JSON arrays based on user prompts.
The tool processes natural language prompts and generates structured JSON data.
"""
from typing import Dict, Any, List
import json
import logging
import re
from .base_tool import BaseTool, tool_function

class JsonArrayTool(BaseTool):
    """
    Tool that creates JSON arrays based on user prompts.
    This tool takes a natural language prompt and converts it into a structured JSON array.
    """
    
    def __init__(self):
        """Initialize the JSON array creation tool."""
        super().__init__(name="JsonArrayTool")
    
    def _execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implements the JSON array creation logic.
        
        Args:
            args: Dictionary containing:
                - prompt: The user's natural language prompt describing the desired JSON array
                - schema (optional): A description of the expected JSON schema
        
        Returns:
            Dictionary containing the generated JSON array and status.
        """
        # Extract the prompt and optional schema from args
        prompt = args.get("prompt", "")
        schema = args.get("schema", None)
        
        if not prompt:
            return {
                "error": "No prompt provided",
                "status": "error"
            }
        
        self.logger.info(f"Processing JSON array prompt: {prompt}")
        
        try:
            # Process the prompt to generate a JSON array
            json_array = self._process_prompt_to_json(prompt, schema)
            
            return {
                "json_array": json_array,
                "original_prompt": prompt,
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error creating JSON array: {str(e)}")
            return {
                "error": f"Failed to create JSON array: {str(e)}",
                "status": "error"
            }
    
    def _process_prompt_to_json(self, prompt: str, schema: str = None) -> List[Any]:
        """
        Process the natural language prompt into a JSON array.
        
        Args:
            prompt: The user's prompt describing the desired JSON data
            schema: Optional schema description to guide JSON structure
            
        Returns:
            The generated JSON array
        """
        # Extract key information from the prompt
        prompt_lower = prompt.lower()
        
        # Determine the entity type (what kind of list are we creating)
        entity_type = self._extract_entity_type(prompt_lower)
        
        # Determine the number of items requested
        count = self._extract_count(prompt_lower) or 5  # Default to 5 items
        
        # Determine the fields to include
        fields = self._extract_fields(prompt_lower, entity_type) or self._default_fields_for_entity(entity_type)
        
        # Generate the appropriate JSON array based on the entity type and fields
        if entity_type == "person" or entity_type == "people":
            return self._create_people_array(count, fields)
        elif entity_type == "task" or entity_type == "todo":
            return self._create_tasks_array(count, fields)
        elif entity_type == "product":
            return self._create_products_array(count, fields)
        elif entity_type == "event":
            return self._create_events_array(count, fields)
        elif entity_type == "location" or entity_type == "place":
            return self._create_locations_array(count, fields)
        elif entity_type == "book":
            return self._create_books_array(count, fields)
        elif entity_type == "movie":
            return self._create_movies_array(count, fields)
        elif entity_type == "song" or entity_type == "music":
            return self._create_songs_array(count, fields)
        elif entity_type == "company":
            return self._create_companies_array(count, fields)
        else:
            # Create a generic array based on the prompt
            return self._create_generic_array(count, fields, entity_type)
    
    def _extract_entity_type(self, prompt: str) -> str:
        """Extract the entity type from the prompt."""
        # Common entity type patterns
        entity_patterns = [
            r"list of (\w+)",
            r"array of (\w+)",
            r"json (array|list) of (\w+)",
            r"(\w+) list",
            r"(\w+) array"
        ]
        
        for pattern in entity_patterns:
            match = re.search(pattern, prompt)
            if match:
                if len(match.groups()) == 1:
                    entity = match.group(1)
                else:
                    entity = match.group(2)
                    
                # Convert plural to singular if needed
                if entity.endswith("ies"):
                    entity = entity[:-3] + "y"
                elif entity.endswith("s") and not entity.endswith("ss"):
                    entity = entity[:-1]
                    
                return entity
        
        # If no specific entity type found, use generic
        return "item"
    
    def _extract_count(self, prompt: str) -> int:
        """Extract the requested count from the prompt."""
        # Look for number patterns
        count_patterns = [
            r"(\d+) (?:items|entries)",
            r"list of (\d+)",
            r"array of (\d+)",
            r"(\d+) \w+"
        ]
        
        for pattern in count_patterns:
            match = re.search(pattern, prompt)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    pass
        
        return None
    
    def _extract_fields(self, prompt: str, entity_type: str) -> List[str]:
        """Extract the fields to include from the prompt."""
        # Look for field specifications
        field_patterns = [
            r"with (?:fields|attributes) (?:like|such as) ([\w\s,]+)",
            r"including ([\w\s,]+)",
            r"contains? ([\w\s,]+)",
            r"has ([\w\s,]+)"
        ]
        
        for pattern in field_patterns:
            match = re.search(pattern, prompt)
            if match:
                fields_text = match.group(1)
                # Split by commas or "and"
                fields = re.split(r",|\sand\s", fields_text)
                # Clean up and return
                return [field.strip() for field in fields if field.strip()]
        
        return None
    
    def _default_fields_for_entity(self, entity_type: str) -> List[str]:
        """Provide default fields for common entity types."""
        defaults = {
            "person": ["name", "age", "email"],
            "people": ["name", "age", "email"],
            "task": ["title", "status", "priority"],
            "todo": ["title", "status", "priority"],
            "product": ["name", "price", "category"],
            "event": ["name", "date", "location"],
            "location": ["name", "address", "city"],
            "place": ["name", "address", "city"],
            "book": ["title", "author", "year"],
            "movie": ["title", "director", "year"],
            "song": ["title", "artist", "duration"],
            "music": ["title", "artist", "duration"],
            "company": ["name", "industry", "size"]
        }
        
        return defaults.get(entity_type, ["name", "description"])
    
    def _create_people_array(self, count: int, fields: List[str]) -> List[Dict[str, Any]]:
        """Create an array of people."""
        people = []
        
        first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
        
        roles = ["Developer", "Designer", "Manager", "Engineer", "Analyst", "Consultant", "Director", "Coordinator", "Specialist", "Technician"]
        departments = ["Engineering", "Design", "Marketing", "Sales", "HR", "Finance", "Operations", "Customer Support", "Research", "Product"]
        
        for i in range(count):
            person = {"id": i + 1}
            
            if "name" in fields:
                person["name"] = f"{first_names[i % len(first_names)]} {last_names[i % len(last_names)]}"
            
            if "age" in fields:
                person["age"] = 25 + (i % 30)  # Ages 25-54
            
            if "email" in fields:
                first = first_names[i % len(first_names)].lower()
                last = last_names[i % len(last_names)].lower()
                person["email"] = f"{first}.{last}@example.com"
            
            if "role" in fields:
                person["role"] = roles[i % len(roles)]
            
            if "department" in fields:
                person["department"] = departments[i % len(departments)]
            
            if "phone" in fields:
                person["phone"] = f"555-{100 + i:03d}-{1000 + i:04d}"
            
            people.append(person)
        
        return people
    
    def _create_tasks_array(self, count: int, fields: List[str]) -> List[Dict[str, Any]]:
        """Create an array of tasks."""
        tasks = []
        
        task_titles = [
            "Complete project proposal", "Review code changes", "Deploy application",
            "Fix critical bug", "Implement new feature", "Update documentation",
            "Schedule team meeting", "Conduct user testing", "Optimize database queries",
            "Design user interface"
        ]
        
        statuses = ["pending", "in progress", "completed", "blocked", "deferred"]
        priorities = ["low", "medium", "high", "critical"]
        
        for i in range(count):
            task = {"id": i + 1}
            
            if "title" in fields:
                task["title"] = task_titles[i % len(task_titles)]
            
            if "status" in fields:
                task["status"] = statuses[i % len(statuses)]
            
            if "priority" in fields:
                task["priority"] = priorities[i % len(priorities)]
            
            if "due_date" in fields:
                task["due_date"] = f"2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}"
            
            if "assignee" in fields:
                first_names = ["James", "Mary", "John", "Patricia", "Robert"]
                task["assignee"] = first_names[i % len(first_names)]
            
            tasks.append(task)
        
        return tasks
    
    def _create_products_array(self, count: int, fields: List[str]) -> List[Dict[str, Any]]:
        """Create an array of products."""
        products = []
        
        product_names = [
            "Laptop", "Smartphone", "Headphones", "Wireless Mouse", "Monitor",
            "Keyboard", "Tablet", "Smartwatch", "Printer", "External Hard Drive"
        ]
        
        categories = ["Electronics", "Computers", "Accessories", "Audio", "Mobile"]
        
        for i in range(count):
            product = {"id": f"P{1000 + i:04d}"}
            
            if "name" in fields:
                product["name"] = product_names[i % len(product_names)]
            
            if "price" in fields:
                product["price"] = 49.99 + (i * 50)
            
            if "category" in fields:
                product["category"] = categories[i % len(categories)]
            
            if "stock" in fields:
                product["stock"] = (i + 1) * 10
            
            if "description" in fields:
                product["description"] = f"High-quality {product_names[i % len(product_names)].lower()} for professional use"
            
            products.append(product)
        
        return products
    
    def _create_events_array(self, count: int, fields: List[str]) -> List[Dict[str, Any]]:
        """Create an array of events."""
        events = []
        
        event_names = [
            "Annual Conference", "Product Launch", "Team Building", "Workshop",
            "Webinar", "Hackathon", "Trade Show", "Training Session", "Meeting", "Celebration"
        ]
        
        locations = ["New York", "San Francisco", "Chicago", "Boston", "Seattle", "Austin", "Denver", "Atlanta", "Miami", "Los Angeles"]
        
        for i in range(count):
            event = {"id": i + 1}
            
            if "name" in fields:
                event["name"] = event_names[i % len(event_names)]
            
            if "date" in fields:
                event["date"] = f"2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}"
            
            if "location" in fields:
                event["location"] = locations[i % len(locations)]
            
            if "attendees" in fields:
                event["attendees"] = (i + 1) * 15
            
            if "description" in fields:
                event["description"] = f"A {event_names[i % len(event_names)].lower()} event for professionals"
            
            events.append(event)
        
        return events
    
    def _create_locations_array(self, count: int, fields: List[str]) -> List[Dict[str, Any]]:
        """Create an array of locations."""
        locations = []
        
        location_names = [
            "Central Park", "Golden Gate Park", "Millennium Park", "Boston Common",
            "Pike Place Market", "South Congress", "Red Rocks Park", "Piedmont Park",
            "South Beach", "Griffith Observatory"
        ]
        
        cities = ["New York", "San Francisco", "Chicago", "Boston", "Seattle", "Austin", "Denver", "Atlanta", "Miami", "Los Angeles"]
        
        for i in range(count):
            location = {"id": i + 1}
            
            if "name" in fields:
                location["name"] = location_names[i % len(location_names)]
            
            if "address" in fields:
                location["address"] = f"{100 + i} Main Street"
            
            if "city" in fields:
                location["city"] = cities[i % len(cities)]
            
            if "state" in fields:
                states = ["NY", "CA", "IL", "MA", "WA", "TX", "CO", "GA", "FL", "CA"]
                location["state"] = states[i % len(states)]
            
            if "zipcode" in fields:
                location["zipcode"] = f"{10000 + (i * 1000)}"
            
            locations.append(location)
        
        return locations
    
    def _create_books_array(self, count: int, fields: List[str]) -> List[Dict[str, Any]]:
        """Create an array of books."""
        books = []
        
        book_titles = [
            "The Great Novel", "Code Complete", "Design Patterns", "Data Science Handbook",
            "Modern Architecture", "History of Art", "Future of AI", "Business Strategy",
            "Psychology Principles", "Healthy Living"
        ]
        
        authors = [
            "Jane Smith", "John Doe", "Robert Johnson", "Maria Garcia", "James Wilson",
            "Patricia Moore", "Michael Brown", "Elizabeth Davis", "William Miller", "Jennifer Taylor"
        ]
        
        categories = ["Fiction", "Technology", "Design", "Science", "Architecture", "Art", "Technology", "Business", "Psychology", "Health"]
        
        for i in range(count):
            book = {"id": i + 1}
            
            if "title" in fields:
                book["title"] = book_titles[i % len(book_titles)]
            
            if "author" in fields:
                book["author"] = authors[i % len(authors)]
            
            if "year" in fields:
                book["year"] = 2010 + (i % 13)
            
            if "category" in fields:
                book["category"] = categories[i % len(categories)]
            
            if "pages" in fields:
                book["pages"] = 200 + (i * 50)
            
            if "publisher" in fields:
                publishers = ["Penguin Books", "Random House", "O'Reilly Media", "Addison-Wesley", "McGraw Hill"]
                book["publisher"] = publishers[i % len(publishers)]
            
            books.append(book)
        
        return books
    
    def _create_movies_array(self, count: int, fields: List[str]) -> List[Dict[str, Any]]:
        """Create an array of movies."""
        movies = []
        
        movie_titles = [
            "The Blockbuster", "Award Winner", "Action Adventure", "Comedy Gold",
            "Dramatic Story", "Sci-Fi Journey", "Historical Epic", "Animation Delight",
            "Thriller", "Documentary"
        ]
        
        directors = [
            "Steven Spielberg", "Christopher Nolan", "Martin Scorsese", "Quentin Tarantino",
            "Sofia Coppola", "James Cameron", "Greta Gerwig", "Spike Lee", "Ava DuVernay", "Wes Anderson"
        ]
        
        genres = ["Action", "Drama", "Comedy", "Sci-Fi", "History", "Animation", "Thriller", "Documentary", "Adventure", "Romance"]
        
        for i in range(count):
            movie = {"id": i + 1}
            
            if "title" in fields:
                movie["title"] = movie_titles[i % len(movie_titles)]
            
            if "director" in fields:
                movie["director"] = directors[i % len(directors)]
            
            if "year" in fields:
                movie["year"] = 2010 + (i % 13)
            
            if "genre" in fields:
                movie["genre"] = genres[i % len(genres)]
            
            if "rating" in fields:
                movie["rating"] = round(3.5 + (i % 5) * 0.3, 1)
            
            if "duration" in fields:
                movie["duration"] = 90 + (i * 10)
            
            movies.append(movie)
        
        return movies
    
    def _create_songs_array(self, count: int, fields: List[str]) -> List[Dict[str, Any]]:
        """Create an array of songs."""
        songs = []
        
        song_titles = [
            "Summer Hit", "Winter Ballad", "Rocking Anthem", "Pop Sensation",
            "Jazz Standard", "Classical Piece", "Country Road", "Hip Hop Beat",
            "Electronic Mix", "R&B Groove"
        ]
        
        artists = [
            "The Band", "Solo Artist", "DJ Producer", "Classic Quartet", "Rock Group",
            "Pop Star", "Jazz Ensemble", "Orchestra", "Country Singer", "Rap Collective"
        ]
        
        genres = ["Pop", "Rock", "Jazz", "Classical", "Country", "Hip Hop", "Electronic", "R&B", "Alternative", "Folk"]
        
        for i in range(count):
            song = {"id": i + 1}
            
            if "title" in fields:
                song["title"] = song_titles[i % len(song_titles)]
            
            if "artist" in fields:
                song["artist"] = artists[i % len(artists)]
            
            if "duration" in fields:
                song["duration"] = f"{3 + (i % 4)}:{(10 + (i * 10)) % 60:02d}"
            
            if "genre" in fields:
                song["genre"] = genres[i % len(genres)]
            
            if "year" in fields:
                song["year"] = 2010 + (i % 13)
            
            if "album" in fields:
                albums = ["Greatest Hits", "Debut Album", "Sophomore Release", "Live Recording", "Studio Sessions"]
                song["album"] = albums[i % len(albums)]
            
            songs.append(song)
        
        return songs
    
    def _create_companies_array(self, count: int, fields: List[str]) -> List[Dict[str, Any]]:
        """Create an array of companies."""
        companies = []
        
        company_names = [
            "Tech Innovations", "Global Solutions", "Creative Designs", "Data Systems",
            "Future Industries", "Smart Technologies", "Green Energy", "Financial Group",
            "Health Services", "Education Network"
        ]
        
        industries = ["Technology", "Consulting", "Design", "Data", "Manufacturing", "Energy", "Finance", "Healthcare", "Education", "Retail"]
        
        for i in range(count):
            company = {"id": i + 1}
            
            if "name" in fields:
                company["name"] = company_names[i % len(company_names)]
            
            if "industry" in fields:
                company["industry"] = industries[i % len(industries)]
            
            if "size" in fields:
                sizes = ["Small", "Medium", "Large", "Enterprise", "Startup"]
                company["size"] = sizes[i % len(sizes)]
            
            if "founded" in fields:
                company["founded"] = 1990 + (i * 3)
            
            if "location" in fields:
                locations = ["New York", "San Francisco", "Chicago", "Boston", "Seattle", "Austin", "Denver", "Atlanta", "Miami", "Los Angeles"]
                company["location"] = locations[i % len(locations)]
            
            if "employees" in fields:
                employees = [50, 100, 500, 1000, 5000, 10000, 20000, 50000]
                company["employees"] = employees[i % len(employees)]
            
            companies.append(company)
        
        return companies
    
    def _create_generic_array(self, count: int, fields: List[str], entity_type: str) -> List[Dict[str, Any]]:
        """Create a generic array based on fields and entity type."""
        items = []
        
        for i in range(count):
            item = {"id": i + 1}
            
            for field in fields:
                if field == "name":
                    item[field] = f"{entity_type.capitalize()} {i+1}"
                elif field == "description":
                    item[field] = f"Description for {entity_type} {i+1}"
                elif field == "category":
                    categories = ["Category A", "Category B", "Category C", "Category D", "Category E"]
                    item[field] = categories[i % len(categories)]
                elif field == "price":
                    item[field] = 9.99 + (i * 10)
                elif field == "quantity":
                    item[field] = (i + 1) * 5
                elif field == "date":
                    item[field] = f"2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}"
                else:
                    item[field] = f"{field} {i+1}"
            
            items.append(item)
        
        return items

# Initialize a singleton instance
json_array_tool = JsonArrayTool()

# Function to be registered in the tools/__init__.py
@tool_function
def create_json_array(args: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper function for the JsonArrayTool execute method."""
    return json_array_tool.execute(args) 
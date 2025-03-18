from models.tool_definitions import AgentGoal
from tools.tool_registry import (
    search_fixtures_tool,
    search_flights_tool,
    search_trains_tool,
    book_trains_tool,
    create_invoice_tool,
    find_events_tool,
    midicreationtool_tool,
    json_array_tool,
)

goal_match_train_invoice = AgentGoal(
    tools=[
        search_fixtures_tool,
        search_trains_tool,
        book_trains_tool,
        create_invoice_tool,
    ],
    description="The user wants to book a trip to a city in the UK around the dates of a premier league match. "
    "Help the user find a premier league match to attend, search and book trains for that match and offers to invoice them for the cost of train tickets. "
    "The user lives in London. "
    "Gather args for these tools in order, ensuring you move the user from one tool to the next: "
    "1. SearchFixtures: Search for fixtures for a team within a specified date range. The user might ask questions about the matches dates and locations to decide on where to go. "
    "2. SearchTrains: Search for trains to the city of the match and list them for the customer to choose from "
    "3. BookTrains: Book the train tickets, used to invoice the user for the cost of the train tickets "
    "4. CreateInvoice: Invoices the user for the cost of train tickets, with total and details inferred from the conversation history ",
    starter_prompt="Welcome me, give me a description of what you can do, then ask me for the details you need to begin your job as an agent ",
    example_conversation_history="\n ".join(
        [
            "user: I'd like to travel to a premier league match",
            "agent: Sure! Let's start by finding a match you'd like to attend. I know about Premier League fixtures in the UK. Could you tell me which team and what date range you're interested in?"
            "user: Wolves between mid-April and the first week of May, please."
            "agent: Great! Let's find fixtures for Wolverhampton Wanderers FC between 2025-04-15 and 2025-05-05."
            "user_confirmed_tool_run: <user clicks confirm on SearchFixtures tool, passing the full team name as an input>",
            'tool_result: SearchFixtures responds in this JSON format and the results are parsed by the agent below {"fixtures": [{"awayTeam": "West Ham United FC","date": "2025-04-01","homeTeam": "Wolverhampton Wanderers FC"},...,'
            "agent: I found 4 Wolves matches in May 2025: 1. Man City vs Wolves (Away) - May 3 2. Wolves vs Brighton (Home) - May 10 3. Crystal Palace vs Wolves (Away) - May 18 4. Wolves vs Brentford (Home) - May 25 Which match would you like to attend? I'll help you find trains from London.",
            "user: How about the Man City match",
            "agent: Great! Let's find trains to Manchester and back for the match.",
            "user_confirmed_tool_run: <user clicks confirm on SearchTrains tool>",
            'tool_result: SearchTrains responds in this JSON format and the results are parsed by the agent below: {"journeys": [{"arrival": "Manchester","arrival_time": "2025-04-18T12:11","departure": "London","departure_time": "2025-04-18T11:00","id": "T8049","platform": "1","price": 73.5,"type": "outbound"},',
            "agent: I found several train options for your journey to Manchester including outbound options on May 9 at 11am, 3:30pm and 4:30pm and return options on May 11 at 9am, 11am and 1pm. Which trains would you like to book?",
            "user: I'd like the 11am outbound and 3:30pm return",
            "agent: Sounds good, let's book train tickets for the 11am outbound and 3:30pm return trains on May 9 and May 11, one day before and after the match.",
            "user_confirmed_tool_run: <user clicks confirm on BookTrains tool>",
            'tool_result: BookTrains responds in this JSON format and the results are parsed by the agent belowg [{"booking_reference": "BR10879","journey_id": "T9532,T1027","status": "confirmed"}]',
            "agent: Your train tickets have been booked with the reference ABCD1234. Are you ready to be invoiced for the total cost of the train tickets?",
            "user: Yes, pelase invoice me.",
            "user_confirmed_tool_run: <user clicks confirm on CreateInvoice tool which includes details of the train journey, the match, and the total cost>",
            'tool_result: CreateInvoice responds in this JSON format and the results are parsed by the agent below (including a link to the invoice): {"invoiceStatus": "open","invoiceURL": "https://invoice.stripe.com/i/acct_1NBOLuKVZbzw7QA5/test_YWNjdF8xTkJPTHVLVlpienc3UUE1LF9SbGJlZ2xLMjhlc3lxNzFkVVBXbkswOUlFa2Rna1RxLDEzMDAwMTY4Nw0200RLeJRMlw?s=ap","reference": "F9B01CD7-0001"}',
            "agent: Great! I've generated your invoice for your trains to the Manchester City match on the 10th of May. You can view and pay your invoice at this link: https://invoice.stripe.com/i/acct_1NBOLuKVZbzw7QA5/test_YWNjdF8xTkJPTHVLVlpienc3UUE1LF9SbGJlZ2xLMjhlc3lxNzFkVVBXbkswOUlFa2Rna1RxLDEzMDAwMTY4Nw0200RLeJRMlw?s=ap <this is the end of the chat>",
        ]
    ),
)

# unused
goal_event_flight_invoice = AgentGoal(
    tools=[
        find_events_tool,
        search_flights_tool,
        create_invoice_tool,
    ],
    description="Help the user gather args for these tools in order: "
    "1. FindEvents: Find an event to travel to "
    "2. SearchFlights: search for a flight around the event dates "
    "3. CreateInvoice: Create a simple invoice for the cost of that flight ",
    starter_prompt="Welcome me, give me a description of what you can do, then ask me for the details you need to do your job",
    example_conversation_history="\n ".join(
        [
            "user: I'd like to travel to an event",
            "agent: Sure! Let's start by finding an event you'd like to attend. I know about events in Australia and New Zealand cities. Could you tell me which city and month you're interested in?",
            "user: sydney in may please",
            "agent: Great! Let's find an events in Sydney in May.",
            "user_confirmed_tool_run: <user clicks confirm on FindEvents tool>",
            "tool_result: { 'event_name': 'Vivid Sydney', 'event_date': '2023-05-01' }",
            "agent: Found an event! There's Vivid Sydney on May 1 2025, ending on May 14 2025. Would you like to search for flights around these dates?",
            "user: Yes, please",
            "agent: Let's search for flights around these dates. Could you provide your departure city?",
            "user: San Francisco",
            "agent: Thanks, searching for flights from San Francisco to Sydney around 2023-02-25 to 2023-02-28.",
            "user_confirmed_tool_run: <user clicks confirm on SearchFlights tool>"
            'tool_result: results including {"flight_number": "CX101", "return_flight_number": "CX102", "price": 850.0}',
            "agent: Found some flights! The cheapest is CX101 for $850. Would you like to generate an invoice for this flight?",
            "user_confirmed_tool_run: <user clicks confirm on CreateInvoice tool>",
            'tool_result: { "status": "success", "invoice": { "flight_number": "CX101", "amount": 850.0 }, invoiceURL: "https://example.com/invoice" }',
            "agent: Invoice generated! Here's the link: https://example.com/invoice",
        ]
    ),
)

# Music Creation Goal
music_creation_goal = AgentGoal(
    tools=[
        midicreationtool_tool,
    ],
    description="Help the user create MIDI music by converting musical ideas into MIDI messages. "
    "The MidiCreationTool takes a list of (note, duration) tuples and converts them into MIDI messages. "
    "1. Help the user understand MIDI note numbers (60 = middle C, etc.) "
    "2. Assist with converting musical ideas (e.g., melodies, chords, rhythms) into the required format "
    "3. Guide the user through using the MidiCreationTool to create and hear their musical ideas ",
    starter_prompt="Welcome! I can help you create music with MIDI. Tell me about your musical idea, and I'll help you convert it into MIDI notes and durations that our tool can play.",
    example_conversation_history="\n ".join(
        [
            "user: Can you help me create a simple melody?",
            "agent: Absolutely! I'd be happy to help you create a simple melody using our MIDI Creation Tool. Let me explain how it works: MIDI notes are represented by numbers (60 = middle C, 62 = D, 64 = E, etc.) and durations are in beats (0.25 = sixteenth note, 0.5 = eighth note, 1.0 = quarter note). What kind of melody are you thinking about? A happy tune, something sad, or maybe a specific song?",
            "user: I'd like a happy, simple tune like 'Twinkle Twinkle Little Star'",
            "agent: Great choice! 'Twinkle Twinkle Little Star' is a classic melody. The first part of the melody in C major would be represented as: C C G G A A G (with a rest) F F E E D D C. I'll convert this to MIDI note numbers and durations for you.",
            "user: That sounds perfect!",
            "agent: Here's the melody for 'Twinkle Twinkle Little Star' in MIDI format: [60, 0.5], [60, 0.5], [67, 0.5], [67, 0.5], [69, 0.5], [69, 0.5], [67, 1.0], [0, 0.25], [65, 0.5], [65, 0.5], [64, 0.5], [64, 0.5], [62, 0.5], [62, 0.5], [60, 1.0]. Would you like me to use the MidiCreationTool to convert this into playable MIDI?",
            "user_confirmed_tool_run: <user clicks confirm on MidiCreationTool>",
            "tool_result: {\"result\": [{\"type\": \"note_on\", \"note\": 60, \"velocity\": 64, \"time\": 0}, {\"type\": \"note_off\", \"note\": 60, \"velocity\": 0, \"time\": 240}], \"status\": \"success\", \"midi_data\": {\"format\": 0, \"ticks_per_beat\": 480, \"tracks\": 1, \"messages_count\": 30}}",
            "agent: Great! I've converted your melody to MIDI. You can now play it back using the 'Play MIDI' button. The melody has 1 track with 30 MIDI messages that represent the notes of 'Twinkle Twinkle Little Star'. How does it sound? Would you like to modify it or try a different melody?",
            "user: It sounds good! Can we try a simple chord progression?",
            "agent: Absolutely! Let's create a simple C major chord progression: C - F - G - C (I - IV - V - I). Each chord will be played as a triad (3 notes played simultaneously). I'll prepare the MIDI data for this progression.",
            "user: Perfect!",
        ]
    ),
)

# JSON Array Creation Goal
json_array_creation_goal = AgentGoal(
    tools=[
        json_array_tool,
    ],
    description="Help the user create structured JSON arrays based on natural language prompts. "
    "The CreateJsonArray tool takes a natural language prompt and converts it into a structured JSON array. "
    "1. Help the user understand what kind of data they want to structure "
    "2. Assist with converting their requirements into clear prompts "
    "3. Guide the user through using the CreateJsonArray tool to create JSON data from their descriptions ",
    starter_prompt="Welcome! I can help you create structured JSON arrays from your descriptions. Tell me what kind of data you'd like to structure, and I'll help you convert it into a proper JSON array format.",
    example_conversation_history="\n ".join(
        [
            "user: I need to create a JSON list of tasks",
            "agent: I'd be happy to help you create a JSON array of tasks! The CreateJsonArray tool can convert your description into a structured JSON format. Could you tell me more about what kind of tasks you want to include? For example, do you need fields like title, status, due date, priority, etc?",
            "user: Yes, I need tasks with a title, priority level (high, medium, low), and status (pending, in progress, completed)",
            "agent: Great! I'll help you create a JSON array of tasks with those fields. I'll use the CreateJsonArray tool to generate this for you. Would you like me to generate a sample list, or do you have specific tasks you want to include?",
            "user: Please generate a sample list of 5 tasks related to website development",
            "agent: I'll create a sample JSON array of 5 website development tasks with title, priority, and status fields. Let me use the CreateJsonArray tool to generate this for you.",
            "user_confirmed_tool_run: <user clicks confirm on CreateJsonArray tool>",
            'tool_result: {"json_array": [{"id": 1, "title": "Set up development environment", "priority": "high", "status": "completed"}, {"id": 2, "title": "Design website mockups", "priority": "high", "status": "completed"}, {"id": 3, "title": "Implement responsive layout", "priority": "medium", "status": "in progress"}, {"id": 4, "title": "Create user authentication system", "priority": "high", "status": "pending"}, {"id": 5, "title": "Deploy website to staging server", "priority": "medium", "status": "pending"}], "status": "success"}',
            "agent: Here's your JSON array of website development tasks:\n```json\n[\n  {\n    \"id\": 1,\n    \"title\": \"Set up development environment\",\n    \"priority\": \"high\",\n    \"status\": \"completed\"\n  },\n  {\n    \"id\": 2,\n    \"title\": \"Design website mockups\",\n    \"priority\": \"high\",\n    \"status\": \"completed\"\n  },\n  {\n    \"id\": 3,\n    \"title\": \"Implement responsive layout\",\n    \"priority\": \"medium\",\n    \"status\": \"in progress\"\n  },\n  {\n    \"id\": 4,\n    \"title\": \"Create user authentication system\",\n    \"priority\": \"high\",\n    \"status\": \"pending\"\n  },\n  {\n    \"id\": 5,\n    \"title\": \"Deploy website to staging server\",\n    \"priority\": \"medium\",\n    \"status\": \"pending\"\n  }\n]\n```\nIs this what you were looking for? Would you like to make any changes or generate a different type of JSON array?",
            "user: This is perfect! Can I also get a JSON array for a list of team members?",
            "agent: Absolutely! I'd be happy to create a JSON array for a list of team members. What information would you like to include for each team member? Common fields might include name, role, email, department, etc.",
        ]
    ),
)

# Unified Multi-Tool Agent Goal
unified_agent_goal = AgentGoal(
    tools=[
        # Travel and events tools
        find_events_tool,
        search_flights_tool,
        search_fixtures_tool,
        search_trains_tool,
        book_trains_tool,
        create_invoice_tool,
        
        # Creative tools
        midicreationtool_tool,
        
        # Data tools
        json_array_tool,
    ],
    description="You are a helpful assistant that can use a variety of tools to help users with different tasks. "
    "You should identify what the user needs and select the most appropriate tool based on their request. "
    "Available capabilities include: "
    "1. Finding events in Oceania cities "
    "2. Searching for flights between destinations "
    "3. Finding UK premier league fixtures "
    "4. Searching and booking train tickets in the UK "
    "5. Creating invoices for travel expenses "
    "6. Creating MIDI music from user descriptions "
    "7. Creating structured JSON arrays from user descriptions "
    "Analyze the user's request carefully to determine which capability is most relevant, and guide them through using the appropriate tool.",
    starter_prompt="Welcome! I'm your AI assistant that can help with various tasks. I can find events, search for flights and trains, create invoices, compose MIDI music, and generate structured JSON data. Just let me know what you'd like to do, and I'll assist you with the right tools for your task.",
    example_conversation_history="\n ".join(
        [
            "user: I'd like to create some music",
            "agent: I'd be happy to help you create music! I can convert musical ideas into MIDI format. Let me explain how it works: MIDI notes are represented by numbers (60 = middle C, 62 = D, 64 = E, etc.) and durations are in beats (0.25 = sixteenth note, 0.5 = eighth note, 1.0 = quarter note). What kind of melody are you thinking about? A happy tune, something sad, or maybe a specific song?",
            "user: Something like Twinkle Twinkle Little Star",
            "agent: Great choice! 'Twinkle Twinkle Little Star' is a classic melody. The first part in C major would be: C C G G A A G (with a rest) F F E E D D C. I'll convert this to MIDI note numbers and durations for you: [60, 0.5], [60, 0.5], [67, 0.5], [67, 0.5], [69, 0.5], [69, 0.5], [67, 1.0], [0, 0.25], [65, 0.5], [65, 0.5], [64, 0.5], [64, 0.5], [62, 0.5], [62, 0.5], [60, 1.0]. Would you like me to use the MidiCreationTool to convert this into playable MIDI?",
            "user_confirmed_tool_run: <user clicks confirm on MidiCreationTool>",
            "tool_result: {\"result\": [{\"type\": \"note_on\", \"note\": 60, \"velocity\": 64, \"time\": 0}, {\"type\": \"note_off\", \"note\": 60, \"velocity\": 0, \"time\": 240}], \"status\": \"success\", \"midi_data\": {\"format\": 0, \"ticks_per_beat\": 480, \"tracks\": 1, \"messages_count\": 30}}",
            "agent: Great! I've converted your melody to MIDI. You can now play it back. The melody has 1 track with 30 MIDI messages. How does it sound?",
            "user: That's nice! Now I'd like to plan a trip to a soccer match in the UK.",
            "agent: I'd be happy to help you plan a trip to a soccer match in the UK! I can help find Premier League fixtures and train tickets. Do you have a specific team you'd like to see play? And what timeframe are you considering for your trip?",
            "user: I'm interested in seeing Liverpool play in March.",
            "agent: Great choice! Let me check Premier League fixtures for Liverpool FC in March. I'll search for matches between 2025-03-01 and 2025-03-31.",
            "user_confirmed_tool_run: <user clicks confirm on SearchFixtures tool>",
            'tool_result: {"fixtures": [{"awayTeam": "Liverpool FC","date": "2025-03-08","homeTeam": "Manchester United FC"}, {"awayTeam": "Brighton & Hove Albion FC","date": "2025-03-15","homeTeam": "Liverpool FC"}, {"awayTeam": "Liverpool FC","date": "2025-03-22","homeTeam": "Chelsea FC"}]}',
            "agent: I found 3 Liverpool matches in March 2025: 1. Liverpool at Manchester United - March 8 (Away) 2. Liverpool vs Brighton - March 15 (Home at Anfield) 3. Liverpool at Chelsea - March 22 (Away). Which match would you like to attend?",
            "user: Actually, can we switch topics? I need to create a JSON list of products.",
            "agent: Absolutely! I'd be happy to help you create a JSON array of products. The CreateJsonArray tool can convert your description into a structured JSON format. Could you tell me more about what information you want to include for each product? Common fields include name, price, category, description, etc.",
            "user: I need products with name, price, and stock quantity - about 3 electronic items.",
            "agent: I'll create a JSON array of 3 electronic products with name, price, and stock quantity. Let me use the CreateJsonArray tool to generate this for you.",
            "user_confirmed_tool_run: <user clicks confirm on CreateJsonArray tool>",
            'tool_result: {"json_array": [{"id": "P1001", "name": "Laptop", "price": 999.99, "stock": 10}, {"id": "P1002", "name": "Smartphone", "price": 699.99, "stock": 20}, {"id": "P1003", "name": "Headphones", "price": 149.99, "stock": 30}], "status": "success"}',
            "agent: Here's your JSON array of electronic products:\n```json\n[\n  {\n    \"id\": \"P1001\",\n    \"name\": \"Laptop\",\n    \"price\": 999.99,\n    \"stock\": 10\n  },\n  {\n    \"id\": \"P1002\",\n    \"name\": \"Smartphone\",\n    \"price\": 699.99,\n    \"stock\": 20\n  },\n  {\n    \"id\": \"P1003\",\n    \"name\": \"Headphones\",\n    \"price\": 149.99,\n    \"stock\": 30\n  }\n]\n```\nIs this what you were looking for?",
        ]
    ),
)

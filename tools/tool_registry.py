from models.tool_definitions import ToolDefinition, ToolArgument


# Add HelpTool definition
help_tool = ToolDefinition(
    name="HelpTool",
    description="Provides information about available tools and answers questions about the system.",
    arguments=[
        ToolArgument(
            name="query",
            type="string",
            description="The help query (e.g., 'list all tools', 'how to use SearchFlights', etc.)",
        ),
    ],
)

# Add DefaultChatTool at the top
default_chat_tool = ToolDefinition(
    name="DefaultChatTool",
    description="Processes user messages and decides whether to respond directly or trigger specialized tools. This is the main chat interface for the agent.",
    arguments=[
        ToolArgument(
            name="message",
            type="string",
            description="The user's message to process",
        ),
        ToolArgument(
            name="conversation_history",
            type="array",
            description="Optional array of previous conversation turns for context",
        ),
    ],
)

midicreationtool_tool = ToolDefinition(
    name="MidiCreationTool",
    description="Converts a text representation of music (a list of note-duration tuples) into MIDI messages. Each tuple contains a note value (MIDI note number 21-108, or 0 for silence) and a duration value (float between 0 and 2, where 1.0 represents a quarter note).",
    arguments=[
        ToolArgument(
            name="music_text",
            type="list",
            description="A list of tuples where each tuple is (note, duration). 'note' is an integer (21-108 for a valid note, or 0 for silence) and 'duration' is a float (0 to 2, where 1.0 represents a quarter note).",
        ),
    ],
)

# JSON Array Tool definition
json_array_tool = ToolDefinition(
    name="CreateJsonArray",
    description="Creates a JSON array based on a natural language prompt. The tool can interpret various types of structured data requests and generate appropriate JSON arrays.",
    arguments=[
        ToolArgument(
            name="prompt",
            type="string",
            description="Natural language description of the JSON array to be created, such as 'Create a list of tasks', 'Generate a list of people', etc.",
        ),
        ToolArgument(
            name="schema",
            type="string",
            description="Optional description of the expected schema for the JSON array (e.g., fields and data types).",
        ),
    ],
)

search_flights_tool = ToolDefinition(
    name="SearchFlights",
    description="Search for return flights from an origin to a destination within a date range (dateDepart, dateReturn).",
    arguments=[
        ToolArgument(
            name="origin",
            type="string",
            description="Airport or city (infer airport code from city and store)",
        ),
        ToolArgument(
            name="destination",
            type="string",
            description="Airport or city code for arrival (infer airport code from city and store)",
        ),
        ToolArgument(
            name="dateDepart",
            type="ISO8601",
            description="Start of date range in human readable format, when you want to depart",
        ),
        ToolArgument(
            name="dateReturn",
            type="ISO8601",
            description="End of date range in human readable format, when you want to return",
        ),
    ],
)

# Example class-based tool definition
example_tool_class_tool = ToolDefinition(
    name="ExampleToolClass",
    description="Example tool that demonstrates the class-based approach. Takes a message and returns it with a greeting.",
    arguments=[
        ToolArgument(
            name="message",
            type="string",
            description="The message to greet (defaults to 'World')",
        ),
    ],
)

# Example function-based tool definition
example_tool_function_tool = ToolDefinition(
    name="ExampleToolFunction",
    description="Example tool that demonstrates the function-based approach. Takes a message and returns it with a farewell.",
    arguments=[
        ToolArgument(
            name="message",
            type="string",
            description="The message to bid farewell to (defaults to 'World')",
        ),
    ],
)

search_trains_tool = ToolDefinition(
    name="SearchTrains",
    description="Search for trains between two English cities. Returns a list of train information for the user to choose from.",
    arguments=[
        ToolArgument(
            name="origin",
            type="string",
            description="The city or place to depart from",
        ),
        ToolArgument(
            name="destination",
            type="string",
            description="The city or place to arrive at",
        ),
        ToolArgument(
            name="outbound_time",
            type="ISO8601",
            description="The date and time to search for outbound trains. If time of day isn't asked for, assume a decent time of day/evening for the outbound journey",
        ),
        ToolArgument(
            name="return_time",
            type="ISO8601",
            description="The date and time to search for return trains. If time of day isn't asked for, assume a decent time of day/evening for the inbound journey",
        ),
    ],
)

book_trains_tool = ToolDefinition(
    name="BookTrains",
    description="Books train tickets. Returns a booking reference.",
    arguments=[
        ToolArgument(
            name="train_ids",
            type="string",
            description="The IDs of the trains to book, comma separated",
        ),
    ],
)

create_invoice_tool = ToolDefinition(
    name="CreateInvoice",
    description="Generate an invoice for the items described for the total inferred by the conversation history so far. Returns URL to invoice.",
    arguments=[
        ToolArgument(
            name="amount",
            type="float",
            description="The total cost to be invoiced. Infer this from the conversation history.",
        ),
        ToolArgument(
            name="tripDetails",
            type="string",
            description="A description of the item details to be invoiced, inferred from the conversation history.",
        ),
    ],
)

search_fixtures_tool = ToolDefinition(
    name="SearchFixtures",
    description="Search for upcoming fixtures for a given team within a date range inferred from the user's description. Valid teams this 24/25 season are Arsenal FC, Aston Villa FC, AFC Bournemouth, Brentford FC, Brighton & Hove Albion FC, Chelsea FC, Crystal Palace FC, Everton FC, Fulham FC, Ipswich Town FC, Leicester City FC, Liverpool FC, Manchester City FC, Manchester United FC, Newcastle United FC, Nottingham Forest FC, Southampton FC, Tottenham Hotspur FC, West Ham United FC, Wolverhampton Wanderers FC",
    arguments=[
        ToolArgument(
            name="team",
            type="string",
            description="The full name of the team to search for.",
        ),
        ToolArgument(
            name="date_from",
            type="string",
            description="The start date in format (YYYY-MM-DD) for the fixture search inferred from the user's request (e.g. mid-March).",
        ),
        ToolArgument(
            name="date_to",
            type="string",
            description="The end date in format (YYYY-MM-DD) for the fixture search (e.g. 'the last week of May').",
        ),
    ],
)

find_events_tool = ToolDefinition(
    name="FindEvents",
    description="Find upcoming events to travel to a given city (e.g., 'Melbourne') and a date or month. "
    "It knows about events in Oceania only (e.g. major Australian and New Zealand cities). "
    "It will search 1 month either side of the month provided. "
    "Returns a list of events. ",
    arguments=[
        ToolArgument(
            name="city",
            type="string",
            description="Which city to search for events",
        ),
        ToolArgument(
            name="month",
            type="string",
            description="The month to search for events (will search 1 month either side of the month provided)",
        ),
    ],
)

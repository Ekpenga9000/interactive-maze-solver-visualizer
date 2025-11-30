"""
Quick verification script showing the variety of start/end scenarios
"""

from compatibility import LegacyMazeGenerator

def show_position_variety():
    """Show examples of the variety of start/end position combinations"""
    print("Examples of Randomized Start/End Position Combinations:")
    print("=" * 55)
    
    generator = LegacyMazeGenerator(21, 21)  # Same size as main app
    
    scenarios = [
        "Corner to Corner",
        "Corner to Center", 
        "Center to Edge",
        "Edge to Edge",
        "Center to Corner"
    ]
    
    for i, scenario_type in enumerate(scenarios):
        maze, start, end = generator.generate_with_positions(randomize_positions=True)
        
        # Categorize the positions
        def categorize_position(pos, width=21, height=21):
            x, y = pos
            center_x, center_y = width // 2, height // 2
            
            # Check if it's a corner
            if (x == 1 or x == width - 2) and (y == 1 or y == height - 2):
                return "Corner"
            # Check if it's center
            elif abs(x - center_x) <= 1 and abs(y - center_y) <= 1:
                return "Center"
            # Check if it's an edge
            elif x == 1 or x == width - 2 or y == 1 or y == height - 2:
                return "Edge"
            else:
                return "Interior"
        
        start_type = categorize_position(start)
        end_type = categorize_position(end)
        distance = abs(end[0] - start[0]) + abs(end[1] - start[1])
        
        print(f"{i+1}. Start: {start} ({start_type}) → End: {end} ({end_type})")
        print(f"   Manhattan Distance: {distance}")
        print(f"   Scenario: {start_type} to {end_type}")
        print()

if __name__ == "__main__":
    show_position_variety()
    print("✓ Each 'Generate new maze' (G key) will create a different scenario!")
    print("✓ This tests algorithms across varied difficulty levels!")
    print("✓ Watch how different algorithms perform on short vs. long paths!")
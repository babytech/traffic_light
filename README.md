# Traffic Light Simulation Program

This code implements a traffic light simulation program with interactive visualization. 

## 1. Core Purpose

Simulates real-world traffic light operations and demonstrates:
- Vehicle movement rules (stop at red/yellow, go at green)
- Pedestrian crossing behavior (cross at red, wait at green/yellow)
- Traffic light state transitions (green → yellow → red cycles)
- Interactive visualization of traffic flows

## 2. Key Components

### a. MoveObject Class
```python
class MoveObject:
    # Handles movement logic for both vehicles and pedestrians
    def update(self, signal_color):
        # Vehicles (left/right direction)
        if direction in ["right", "left"]:
            if signal_color != "green":
                # Implement gradual stopping before stop line
                # Continue movement if already passed stop line

        # Pedestrians (up/down direction) 
        elif direction in ["down", "up"]:
            if signal_color != "red":
                # Implement waiting behavior
                # Cross normally during red light
```

### b. Traffic Light Control
```python
def light_thread(obj_lists):
    # Controls light cycle timing
    while True:
        # Green: 0-1000 counts (~5s)
        # Yellow: 1000-1300 counts (~1.5s)
        # Red: 1300-3200 counts (~9.5s)
        # Updates all objects' positions
```

### c. User Interface
```python
def starting_screen(_background, _font):
    # Interactive menu with Play/Exit buttons
    # Handles mouse hover effects and click events

# Main rendering loop
while True:
    # Draws appropriate background based on light state
    # Updates vehicle/pedestrian positions
    # Displays traffic light images
```

## 3. Technical Features

### Multi-threaded Architecture
- Dedicated thread for traffic light timing
- Main thread handles UI rendering (60 FPS)

### Object Recycling System
```python
# Vehicles/pedestrians reappear at start point
if self._x > self._end + self._item.get_width():
    self._x = self._begin - self._item.get_width()
```

### Realistic Behavior Simulation
- Gradual deceleration before stop lines
- Different rules for vehicles/pedestrians
- Stop line boundary detection

### Visual Configuration System
```python
# Configurable image resources
image_dict = {
    "highway_red.png": "standard",
    "car_yellow.png": "alpha",
    # ... Other assets ...
}
```

## 4. Educational Value
- Demonstrates fundamental traffic rules
- Visualizes traffic light timing impact
- Shows interaction between road users
- Provides basis for traffic management studies

## 5. Extensibility
Easy to add new features:
- Multiple intersection support
- Emergency vehicle priority
- Traffic flow statistics
- Customizable light timing patterns
- Sound effects for accessibility

This program serves as an effective educational tool for understanding traffic systems, while providing a foundation for more complex traffic simulation development.


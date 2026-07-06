import numpy as np
import random


class QuantumChargeAI:
    def __init__(self):
        self.choices = ["drive", "charge_A", "charge_B", "charge_C", "slow_down"]

    def get_environment_state(self, SoC, stations, traffic, distance):
        """Receive simulation environment data"""
        self.soc = SoC
        self.station_data = stations  # [{station_id, distance, queue_time}]
        self.traffic = traffic
        self.distance_left = distance

    def collapse_wavefunction(self):
        """Use probabilistic model to collapse superposition"""
        probabilities = []

        for choice in self.choices:
            if choice.startswith("charge"):
                station = choice.split("_")[1]
                queue_time = self.get_queue_time(station)
                dist = self.get_station_distance(station)

                prob = self.charge_probability(dist, queue_time)
            elif choice == "slow_down":
                prob = 0.2 if self.soc < 30 else 0.05
            else:
                prob = 1.0 - (self.soc / 100)

            probabilities.append(prob)

        # Normalize probabilities to form valid distribution
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        # Simulate wavefunction collapse
        collapsed_choice = random.choices(self.choices, probabilities)[0]
        return collapsed_choice

    def charge_probability(self, distance, queue_time):
        if queue_time == 0:
            queue_time = 1  # avoid division by zero
        return 1 / (distance * queue_time + 1)

    def get_station_distance(self, station_id):
        return next((s['distance'] for s in self.station_data if s['station_id'] == station_id), 100)

    def get_queue_time(self, station_id):
        return next((s['queue_time'] for s in self.station_data if s['station_id'] == station_id), 10)


# Example integration with CarMaker (IPGControl via socket or API)
def main_decision_loop():
    qai = QuantumChargeAI()

    while True:
        SoC = get_soc_from_carmaker()
        stations = get_charging_station_data()
        traffic = get_traffic_status()
        dist = get_remaining_distance()

        qai.get_environment_state(SoC, stations, traffic, dist)
        action = qai.collapse_wavefunction()

        apply_action_to_simulation(action)

        wait(10)  # run every 10 seconds


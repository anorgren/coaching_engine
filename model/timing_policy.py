"""Policies for selecting the most optimal time to sample."""
from abc import ABC

import numpy as np
from collections import defaultdict


# The time windows in which the recommendation can be sent, the value is the hour at which the 2hour window begins
DEFAULT_SEND_TIME_WINDOWS = (7, 9, 11, 13, 15, 17, 19, 21)


class TimingPolicy(ABC):
    """
    Base class for timing policies.
    """

    def select_hour(self) -> int:
        """
        Select the next hour to sample.

        Returns:
            int: The selected hour.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def update(self, hour: int, reward: int) -> None:
        """
        Update the policy based on the reward received.

        Args:
            hour (int): The hour for which the reward was received.
            reward (int): The reward received.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")


class ThompsonSamplerTimingPolicy(TimingPolicy):
    """
    Thompson Sampling Timing Policy for selecting the next time to sample.

    This is a simple implementation that considers the success of samples across the whole user base.
    A more sophisticated implementation would consider the success of samples for each user to take
    into account differences in user behavior, e.g. cultural, age, behavioral, etc.
    """

    def __init__(self, hours=DEFAULT_SEND_TIME_WINDOWS):
        """
        Initialize the ThompsonSamplerTimingPolicy.

        Args:
            hours: a list of integers representing the hours of the day to sample.
        """
        self.hours = hours
        self.alpha = defaultdict(lambda: 1)
        self.beta = defaultdict(lambda: 1)

    def select_hour(self) -> int:
        """
        Select the next hour to sample based on Thompson Sampling alg.

        Returns:
            int: The selected hour.
        """
        samples = {
            h: np.random.beta(self.alpha[h], self.beta[h])
            for h in self.hours
        }

        return max(samples, key=samples.get)

    def update(self, hour: int, reward: int) -> None:
        """
        Update the alpha and beta parameters based on the reward received.

        Args:
            hour (int): The hour for which the reward was received.
            reward (int): The reward received.
        """
        self.alpha[hour] += reward
        self.beta[hour] += 1 - reward


# simple singleton approach
thompson_timing_policy = ThompsonSamplerTimingPolicy()

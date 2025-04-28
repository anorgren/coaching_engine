from typing import Optional

from ..dto import TimingPolicyType
from ..model import TimingPolicy, thompson_timing_policy


class TimingPolicyFactory:
    """
    Factory class for creating timing policies.
    """

    POLICY_TYPE_TO_POLICY = {
        TimingPolicyType.THOMPSON_SAMPLING: thompson_timing_policy,
    }

    @staticmethod
    def create_timing_policy(
            policy_type: TimingPolicyType | str,
            user_id: Optional[str] = None
    ) -> TimingPolicy:
        """
        Create a timing policy based on the given type.

        Args:
            policy_type (str): The type of timing policy to create.
            user_id (Optional[str]): The user ID for which the timing policy is created.

        Returns:
            TimingPolicy: An instance of the specified timing policy.
        """
        if isinstance(policy_type, str):
            policy_type = TimingPolicyType(policy_type)

        policy = TimingPolicyFactory.POLICY_TYPE_TO_POLICY.get(policy_type)

        if policy is None:
            raise ValueError(f"No policy exists for policy of type {policy_type}")

        return policy

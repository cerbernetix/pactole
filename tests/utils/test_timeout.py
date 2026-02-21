"""Unit tests for the Timeout class."""

# pylint: disable=unused-argument,redefined-outer-name

from pactole.utils import Timeout


class TestTimeout:
    """Unit tests for the Timeout class."""

    def test_init_with_start_true(self, fake_time):
        """Test initialization with start=True (default)."""

        timeout = Timeout(5)

        assert timeout.seconds == 5
        assert timeout.started is True
        assert timeout.elapsed == 0.0
        assert timeout.remaining == 5.0
        assert timeout.expired is False

    def test_init_with_start_false(self, fake_time):
        """Test initialization with start=False."""

        timeout = Timeout(5, start=False)

        assert timeout.seconds == 5
        assert timeout.started is False
        assert timeout.elapsed == 0.0
        assert timeout.remaining == 5.0
        assert timeout.expired is False

    def test_seconds_property_getter(self, fake_time):
        """Test getting the seconds property."""

        timeout = Timeout(10)

        assert timeout.seconds == 10

    def test_seconds_property_setter(self, fake_time):
        """Test setting the seconds property."""

        timeout = Timeout(5)
        timeout.seconds = 10

        assert timeout.seconds == 10

    def test_started_property_when_started(self, fake_time):
        """Test started property returns True when timeout is started."""

        timeout = Timeout(5)

        assert timeout.started is True

    def test_started_property_when_not_started(self, fake_time):
        """Test started property returns False when timeout is not started."""

        timeout = Timeout(5, start=False)

        assert timeout.started is False

    def test_elapsed_when_not_started(self, fake_time):
        """Test elapsed returns 0.0 when timeout is not started."""

        timeout = Timeout(5, start=False)

        assert timeout.elapsed == 0.0

    def test_elapsed_when_started(self, fake_time):
        """Test elapsed returns time passed since start."""

        timeout = Timeout(5)
        fake_time.advance(0.1)

        assert timeout.elapsed == 0.1

    def test_remaining_when_not_started(self, fake_time):
        """Test remaining returns full duration when not started."""

        timeout = Timeout(5, start=False)

        assert timeout.remaining == 5.0

    def test_remaining_when_started(self, fake_time):
        """Test remaining returns time left until timeout expires."""

        timeout = Timeout(1)
        fake_time.advance(0.1)

        assert timeout.remaining == 0.9

    def test_remaining_never_negative(self, fake_time):
        """Test remaining never goes below 0.0."""

        timeout = Timeout(0.1)
        fake_time.advance(0.2)

        assert timeout.remaining == 0.0

    def test_expired_when_not_expired(self, fake_time):
        """Test expired returns False when timeout has not expired."""

        timeout = Timeout(5)

        assert timeout.expired is False

    def test_expired_when_expired(self, fake_time):
        """Test expired returns True when timeout has expired."""

        timeout = Timeout(0.1)
        fake_time.advance(0.2)

        assert timeout.expired is True

    def test_expired_when_not_started(self, fake_time):
        """Test expired returns False when timeout is not started."""

        timeout = Timeout(5, start=False)

        assert timeout.expired is False

    def test_start_method(self, fake_time):
        """Test start method starts the timeout."""

        timeout = Timeout(5, start=False)
        assert timeout.started is False

        timeout.start()

        assert timeout.started is True
        assert timeout.elapsed == 0.0
        assert timeout.remaining == 5.0

    def test_start_method_restarts_timer(self, fake_time):
        """Test start method resets the timer."""

        timeout = Timeout(1)
        fake_time.advance(0.1)
        _ = timeout.elapsed

        timeout.start()
        second_elapsed = timeout.elapsed

        assert second_elapsed == 0.0

    def test_reset_method(self, fake_time):
        """Test reset method resets the timer."""

        timeout = Timeout(5)
        fake_time.advance(0.1)
        assert timeout.elapsed == 0.1

        timeout.reset()

        assert timeout.elapsed == 0.0

    def test_reset_maintains_started_state(self, fake_time):
        """Test reset maintains the started state."""

        timeout = Timeout(5)
        timeout.reset()

        assert timeout.started is True

    def test_stop_method(self, fake_time):
        """Test stop method stops the timeout."""

        timeout = Timeout(5)
        fake_time.advance(0.1)

        timeout.stop()

        assert timeout.started is False

    def test_stop_freezes_elapsed_time(self, fake_time):
        """Test stop freezes the elapsed time."""

        timeout = Timeout(5)

        fake_time.advance(0.1)
        assert timeout.elapsed == 0.1

        timeout.stop()
        assert timeout.elapsed == 0.0

        fake_time.advance(0.1)
        assert timeout.elapsed == 0.0

    def test_stop_resets_remaining_to_full_duration(self, fake_time):
        """Test stop resets remaining time to full duration."""

        timeout = Timeout(1)
        fake_time.advance(0.1)
        timeout.stop()

        assert timeout.remaining == 1.0

    def test_stop_prevents_expiration(self, fake_time):
        """Test stop prevents the timeout from expiring."""

        timeout = Timeout(0.1)
        timeout.stop()
        fake_time.advance(0.2)

        assert timeout.expired is False

    def test_workflow_start_stop_start(self, fake_time):
        """Test starting, stopping, and restarting a timeout."""

        timeout = Timeout(5, start=False)
        assert timeout.started is False

        timeout.start()
        assert timeout.started is True
        fake_time.advance(0.1)
        assert timeout.elapsed == 0.1

        timeout.stop()
        assert timeout.started is False
        assert timeout.elapsed == 0.0

        timeout.start()
        assert timeout.started is True
        assert timeout.elapsed == 0.0

    def test_workflow_with_expiration(self, fake_time):
        """Test complete workflow with timeout expiration."""

        timeout = Timeout(0.1)
        assert timeout.expired is False

        fake_time.advance(0.15)

        assert timeout.expired is True
        assert timeout.remaining == 0.0

    def test_workflow_reset_before_expiration(self, fake_time):
        """Test resetting timeout before it expires."""

        timeout = Timeout(0.2)
        fake_time.advance(0.1)
        assert timeout.expired is False

        timeout.reset()
        fake_time.advance(0.1)

        assert timeout.expired is False

    def test_changing_seconds_during_operation(self, fake_time):
        """Test changing timeout duration during operation."""

        timeout = Timeout(1)
        fake_time.advance(0.1)

        timeout.seconds = 2

        assert timeout.seconds == 2
        assert timeout.remaining > 1.8

"""Test arch object."""

from unittest.mock import patch

import pytest

from supervisor.const import CpuArch


@pytest.fixture(name="mock_detect_cpu", autouse=True)
def mock_detect_cpu_fixture():
    """Mock cpu detection."""
    with patch("platform.machine") as detect_mock:
        detect_mock.return_value = "Unknown"
        yield detect_mock


async def test_machine_not_exits(coresys, sys_machine, sys_supervisor):
    """Test fallback when machine is missing."""
    sys_machine.return_value = None
    sys_supervisor.arch = "amd64"
    await coresys.arch.load()

    assert coresys.arch.default == "amd64"
    assert coresys.arch.supported == [CpuArch.AMD64]


async def test_machine_not_exits_in_db(coresys, sys_machine, sys_supervisor):
    """Test fallback when machine is unknown."""
    sys_machine.return_value = "jedi-master-knight"
    sys_supervisor.arch = "amd64"
    await coresys.arch.load()

    assert coresys.arch.default == "amd64"
    assert coresys.arch.supported == [CpuArch.AMD64]


async def test_supervisor_arch(coresys, sys_machine, sys_supervisor):
    """Test supervisor architecture property."""
    sys_machine.return_value = None
    sys_supervisor.arch = "amd64"
    assert coresys.arch.supervisor == "amd64"

    await coresys.arch.load()

    assert coresys.arch.supervisor == "amd64"


async def test_raspberrypi3_64_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for raspberrypi3_64."""
    sys_machine.return_value = "raspberrypi3-64"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]


async def test_raspberrypi_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for raspberrypi."""
    sys_machine.return_value = "raspberrypi"
    sys_supervisor.arch = "armhf"
    await coresys.arch.load()

    assert coresys.arch.default == "armhf"
    assert coresys.arch.supported == [CpuArch.ARMHF]


async def test_raspberrypi4_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for raspberrypi4."""
    sys_machine.return_value = "raspberrypi4"
    sys_supervisor.arch = "armv7"
    await coresys.arch.load()

    assert coresys.arch.default == "armv7"
    assert coresys.arch.supported == [CpuArch.ARMV7]


async def test_raspberrypi4_64_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for raspberrypi4_64."""
    sys_machine.return_value = "raspberrypi4-64"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]


async def test_raspberrypi5_64_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for raspberrypi5_64."""
    sys_machine.return_value = "raspberrypi5-64"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]


async def test_yellow_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for yellow."""
    sys_machine.return_value = "yellow"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]
    assert coresys.arch.is_supported(["aarch64"]) is True
    assert coresys.arch.is_supported(["fooarch"]) is False
    assert coresys.arch.is_supported(["bararch"]) is False
    assert coresys.arch.is_supported(["x86_64"]) is False


async def test_green_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for green."""
    sys_machine.return_value = "green"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]


async def test_odroid_c2_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for odroid-c2."""
    sys_machine.return_value = "odroid-c2"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]


async def test_odroid_c4_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for odroid-c4."""
    sys_machine.return_value = "odroid-c4"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]


async def test_odroid_m1_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for odroid-m1."""
    sys_machine.return_value = "odroid-m1"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]


async def test_odroid_n2_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for odroid-n2."""
    sys_machine.return_value = "odroid-n2"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]


async def test_intel_nuc_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for intel-nuc."""
    sys_machine.return_value = "intel-nuc"
    sys_supervisor.arch = "amd64"
    await coresys.arch.load()

    assert coresys.arch.default == "amd64"
    assert coresys.arch.supported == [CpuArch.AMD64]


@pytest.mark.parametrize(
    ("platform_machine", "arch"),
    [
        ("armv6l", CpuArch.ARMHF),
        ("armv7l", CpuArch.ARMV7),
    ],
)
def test_detect_32bit_arm_cpu(coresys, mock_detect_cpu, platform_machine, arch):
    """Test native CPU detection for 32-bit ARM."""
    mock_detect_cpu.return_value = platform_machine

    assert coresys.arch.detect_cpu() == arch


async def test_qemux86_64_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for qemux86-64."""
    sys_machine.return_value = "qemux86-64"
    sys_supervisor.arch = "amd64"
    await coresys.arch.load()

    assert coresys.arch.default == "amd64"
    assert coresys.arch.supported == [CpuArch.AMD64]


async def test_qemuarm_64_arch(coresys, sys_machine, sys_supervisor):
    """Test arch for qemuarm-64."""
    sys_machine.return_value = "qemuarm-64"
    sys_supervisor.arch = "aarch64"
    await coresys.arch.load()

    assert coresys.arch.default == "aarch64"
    assert coresys.arch.supported == [CpuArch.AARCH64]

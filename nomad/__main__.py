from nomad.log_config import get_logger
from nomad.session import run_session

logger = get_logger(__name__)


def main():
    run_session()


if __name__ == "__main__":
    main()

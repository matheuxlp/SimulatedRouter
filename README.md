# SimulatedRouter

This project simulates a router that is connected to four mock routers. The simulated router can receive a message that is passed through one of the mock routers to the simulated router. The simulated router will then determine the route and send the message to the designated mock router.

## Usage

To use the simulated router with mock routers, follow these steps:

1. Run the `main.py` file:

```
python3 main.py
```

2. In a new terminal window, run the `mock_router.py` file in the `src` folder:

```
python3 src/mock_router.py
```

3. In another new terminal window, run the `ip_packet_sender.py` file in the `src` folder:

```
python3 src/ip_packet_sender.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

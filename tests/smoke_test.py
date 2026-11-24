from app import create_app


def main():
    app = create_app()
    client = app.test_client()

    routes = ["/", "/dashboard", "/jobs", "/analyzer", "/about"]

    for route in routes:
        response = client.get(route)
        print(route, response.status_code)
        assert response.status_code == 200

    print("Smoke test passed.")


if __name__ == "__main__":
    main()

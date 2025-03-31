# `client.py` Module Specification

## Overview
The `client.py` module provides the `eCFSignerClient` class, which communicates with an external XML signing service. It handles authentication, certificate uploads, and XML seed signing as part of the electronic invoicing (e-CF) workflow required by the DGII in the Dominican Republic.

## Classes

### `eCFSignerClient`

#### Constructor
```python
eCFSignerClient(settings)
```
- **settings** (`dict`): Configuration dictionary with service credentials and endpoint information.

#### Methods

##### `authenticate_user(self)`
Authenticates the client using provided credentials and retrieves a JWT token.
- **Endpoint**: `POST /auth/login`
- **Raises**: `requests.HTTPError` on failure

##### `upload_certificate(self, p12_filepath: str, p12_secret: str)`
Uploads a `.p12` digital certificate to the signing service.
- **Parameters**:
  - `p12_filepath`: Path to the `.p12` file
  - `p12_secret`: Certificate password
- **Endpoint**: `POST /upload-p12`
- **Raises**: `requests.HTTPError` on failure

##### `_get_seed(self)`
Internal method to retrieve a seed from the signing service.
- **Endpoint**: `GET /get-seed`
- **Returns**: XML seed as `str`
- **Raises**: `requests.HTTPError` on failure

##### `get_seed(self)`
Gets a seed directly from DGII's external endpoint.
- **Endpoint**: DGII URL
- **Returns**: XML seed as `str`
- **Raises**: `requests.HTTPError` on failure

##### `get_signed_seed(self, path=None)`
Retrieves the DGII seed, sends it for signing, and optionally saves the result.
- **Parameters**:
  - `path`: Optional file path to save the signed seed
- **Returns**: Signed XML `str` or file path

##### `sign_seed(self, seed: str)`
Signs the given XML seed using the external service.
- **Parameters**:
  - `seed`: XML seed string
- **Endpoint**: `POST /sign-xml`
- **Returns**: Signed XML as `str`
- **Raises**: `requests.HTTPError` on failure

## Helper Functions

### `remove_seed(seedpath)`
Deletes a temporary XML seed file from disk.
- **Parameters**:
  - `seedpath`: Path to the file to delete
- **Returns**: The deleted file path

## Configuration

Default settings are provided via a dictionary:
```python
{
  "service_url": "ecf.example.com",
  "scheme": ["http" | "https"],
  "port": 8080,
  "username": "usrname",
  "password": "passwd",
  "client": "ABC, S. R. L."
}
```

## Dependencies

- `requests`: For HTTP communication
- `frappe`: Used for dictionary utilities and job queuing

## Notes

- Temporary files are written to `/tmp` and removed using a background job via `frappe.enqueue`.
- JWT tokens are used for authorization headers with the signing service.

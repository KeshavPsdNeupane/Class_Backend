from fastapi import HTTPException, status

class HttpErrorMessages:
    USER_NOT_FOUND_404 = "User not found"
    INCORRECT_PASSWORD_BAD_REQ_400 = "Incorrect Password"
    ACCESS_TOKEN_EXPIRED_UN_AUTH_401 = "Access Token Expired"
    REFRESH_TOKEN_EXPIRED_UN_AUTH_401 = "Refresh Token Expired"
    ACCESS_TOKEN_INVALID_UN_AUTH_401 = "Access Token Invalid"
    REFRESH_TOKEN_INVALID_UN_AUTH_401 = "Refresh Token Invalid"
    INVALID_CREDENTIAL_UN_AUTH_401 = "Invalid Credential"
    SESSION_BUSY_CONFLICT_409 = "Current Session is busy"
    EMAIL_CONFLICT_409 = "Email already exists"
    
    @staticmethod
    def INVALID_ROLE_FORBIDDEN_403(role_name: str) -> str:
        return f"Access denied: your role '{role_name}' does not have permission."

    @staticmethod
    def REFERENTIAL_INTEGRITY_UNPROCESSABLE_422(reference_name: str = '') -> str:
        return f"Referential integrity {reference_name} Invalid"

    @staticmethod
    def SOMETHING_NOTFOUND_404(key: str, value: str) -> str:
        return f"{key} : {value} does not exist"
    
    @staticmethod
    def INPUTFIELD_EMPTY_BADREQUEST_400(before_require: str = '' ,after_require: str = '' ) -> str:
        return f"{before_require} is required {after_require}"


class CustomHttpError:
    @staticmethod
    def Unauthorized_401(detail: str = "Request Unauthorized") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
    
    @staticmethod
    def NotFound_404(detail: str = "Request Not Found") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )
    
    @staticmethod
    def Conflict_409(detail: str = "Conflicting Request") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

    @staticmethod
    def BadRequest_400(detail: str = "Bad Request") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
    
    @staticmethod
    def InternalServerError_500(detail: str = "Internal Server Error") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

    @staticmethod
    def ServiceUnavailable_503(detail: str = "Service unavailable") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )
    
    @staticmethod
    def Forbidden_403(detail: str = 'Forbidden Request') -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

    @staticmethod
    def UnprocessableEntity_422(detail: str = 'Unprocessable Request') -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )

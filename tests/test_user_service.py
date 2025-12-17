import pytest
from unittest.mock import Mock, MagicMock
from app.service.user_service import UserService
from app.repository.user_repo import UserRepository
from app.models.entities.user import User
from app.exceptions import UserNotFoundError, EmailNotAllowedNameExistsError
from datetime import datetime


class TestUserService:
    def setup_method(self):
        """각 테스트 메서드 실행 전에 mock repository와 service 인스턴스 생성"""
        self.mock_repo = Mock(spec=UserRepository)
        self.service = UserService(self.mock_repo)

    def test_create_user_success(self):
        """사용자 생성 성공 테스트"""
        # Given
        name = "김테스트"
        email = "test@example.com"
        expected_user = User(id=1, name=name, email=email, created_at=datetime.now())
        
        self.mock_repo.find_by_email.return_value = None
        self.mock_repo.save.return_value = expected_user
        
        # When
        result = self.service.create_user(name, email)
        
        # Then
        assert result == expected_user
        self.mock_repo.save.assert_called_once_with(name=name, email=email)

    def test_get_user_by_id_not_found(self):
        """존재하지 않는 ID로 사용자 조회 시 예외 발생 테스트"""
        # Given
        user_id = 999
        self.mock_repo.find_by_id.return_value = None
        
        # When & Then
        with pytest.raises(UserNotFoundError):
            self.service.get_user(user_id)
        
        self.mock_repo.find_by_id.assert_called_once_with(user_id=user_id)



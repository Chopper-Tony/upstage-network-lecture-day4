from datetime import datetime
from app.repository.user_repo import UserRepository
from app.models.entities.user import User


class TestUserRepository:
    def setup_method(self):
        """각 테스트 메서드 실행 전에 새로운 repository 인스턴스 생성"""
        self.repo = UserRepository()

    def test_save_user_success(self):
        """사용자 저장 성공 테스트"""
        name = "김테스트"
        email = "test@example.com"
        
        user = self.repo.save(name, email)
        
        assert user.id == 1
        assert user.name == name
        assert user.email == email
        assert isinstance(user.created_at, datetime)

    def test_user_id_increment(self):
        """사용자 ID 자동 증가 테스트"""
        user1 = self.repo.save("사용자1", "user1@test.com")
        user2 = self.repo.save("사용자2", "user2@test.com")
        user3 = self.repo.save("사용자3", "user3@test.com")

        assert user1.id == 1
        assert user2.id == 2
        assert user3.id == 3
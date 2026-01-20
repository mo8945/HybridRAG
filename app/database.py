import pymysql

# 1. 접속 정보 설정 (본인의 리눅스 서버 정보로 수정 필수!)
DB_CONFIG = {
    'host': '리눅스_서버_IP',      # 예: '192.168.0.10'
    'user': 'root',
    'password': '리눅스_MySQL_비밀번호',
    'db': 'dr_lee_db',             # 리눅스에서 미리 'CREATE DATABASE dr_lee_db;'를 실행해야 합니다.
    'port': 3306,                  # 리눅스 MySQL 기본 포트
    'charset': 'utf8mb4',          # 한글 및 이모지 지원
    'cursorclass': pymysql.cursors.DictCursor
}

def get_connection():
    """데이터베이스에 접속하는 함수"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ 접속 실패: {e}")
        return None

def init_db():
    """테이블(선반)을 생성하는 함수"""
    conn = get_connection()
    if not conn: return

    try:
        with conn.cursor() as cursor:
            # 기존 콘텐츠 저장 (유튜브 자막 등)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS legacy_knowledge (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    video_id VARCHAR(50),
                    title VARCHAR(255),
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # 새로운 지식 저장 (의약 논문 등)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS new_research_db (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    topic VARCHAR(255),
                    summary TEXT,
                    source_url VARCHAR(500),
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()
        print("✅ 리틀약사 지식 베이스 테이블 생성 완료!")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
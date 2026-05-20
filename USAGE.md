# ACTF 3D 디자인 사용 가이드

## 개요
이 가이드는 Blender 4.4 버전에서 ACTF (Android Cyborg Transformers) 3D 디자인을 생성하는 방법을 설명합니다.

## 시스템 요구사항
- Blender 4.4 이상
- Python 3.10 이상 (Blender 내장)
- GPU (Cycles 렌더링을 위한 권장)

## 설치 방법

### 1. Blender 4.4 설치
1. [Blender 공식 웹사이트](https://www.blender.org/download/)에서 Blender 4.4 다운로드
2. 설치 프로그램 실행 및 설치 완료

### 2. 프로젝트 파일 준비
- `actf_design.py` 파일이 프로젝트 폴더에 있는지 확인

## 사용 방법

### 방법 1: Blender Script Editor 사용 (권장)

1. **Blender 실행**
   ```
   Blender 4.4 실행
   ```

2. **Script Editor 열기**
   - 상단 메뉴에서 `Scripting` 탭 클릭
   - 또는 `Shift + F3` 단축키

3. **스크립트 로드**
   - Script Editor에서 `Open` 버튼 클릭
   - `actf_design.py` 파일 선택

4. **스크립트 실행**
   - `Run Script` 버튼 클릭 (재생 아이콘)
   - 또는 `Alt + P` 단축키

5. **결과 확인**
   - 3D 뷰포트에서 생성된 ACTF 모델 확인
   - 콘솔 출력에서 생성 진행 상황 확인

### 방법 2: 텍스트 에디터에서 실행

1. **Blender Python API 사용**
   ```bash
   blender --background --python actf_design.py
   ```

2. **결물 저장**
   - 스크립트에 저장 코드 추가 필요
   - `.blend` 파일로 자동 저장

## 생성된 구조

### 기본 구조 (14개 부품)
- 머리 (Head)
- 목 (Neck)
- 상체 (Torso)
- 어깨 (Shoulders)
- 골반 (Pelvis)
- 팔 상부/하부 (Upper/Forearm Arms)
- 손 (Hands)
- 허벅지/종아리 (Thighs/Calves)
- 발 (Feet)

### 내골격 구조 (7개 부품)
- 척추 (Spine)
- 흉곽 (Ribcage)
- 두개골 내부 (Skull Interior)
- 심장 공간 (Heart Chamber)
- 폐 공간 (Lung Chambers)
- 골반 내부 (Pelvis Chamber)

### 외골격 구조 (16개 부품)
- 헬멧 (Helmet)
- 흉부 갑옷 (Chest Armor)
- 등 갑옷 (Back Armor)
- 어깨 갑옷 (Shoulder Armor)
- 팔 갑옷 (Arm Armor)
- 장갑 (Gauntlets)
- 골반 갑옷 (Pelvic Armor)
- 다리 갑옷 (Leg Armor)
- 부츠 (Boots)

### 에너지 코어 (3개)
- 흉부 코어 (Chest Core)
- 등 코어 (Back Core)
- 골반 코어 (Pelvic Core)

### 관절 구조 (8개)
- 어깨 관절 (Shoulder Joints)
- 팔꿈치 관절 (Elbow Joints)
- 고관절 (Hip Joints)
- 무릎 관절 (Knee Joints)

## 재질 정보

### 그래핀 폴리머 액정 (Graphene Polymer Liquid Crystal)
- **용도**: 주요 외골격 갑옷
- **특성**: 
  - 메탈릭 블루-그레이 색상
  - 높은 금속성 (0.9)
  - 중간 거칠기 (0.3)
  - 높은 굴절률 (2.4)

### 탄소나노튜브 (Carbon Nanotube)
- **용도**: 강화 부품 (어깨, 장갑, 부츠, 관절)
- **특성**:
  - 검은색
  - 완전 금속성 (1.0)
  - 낮은 거칠기 (0.1)
  - 매우 높은 굴절률 (2.6)

### 내골격 재질 (Internal Skeleton)
- **용도**: 내부 구조물
- **특성**:
  - 흰색-회색
  - 중간 금속성 (0.3)
  - 중간 거칠기 (0.5)
  - 표면 산란 (0.2)

### 에너지 코어 (Energy Core)
- **용도**: 에너지 발생 장치
- **특성**:
  - 청록색 발광
  - 높은 발광 강도 (5.0)

## 렌더링 설정

### 기본 설정
- **렌더 엔진**: Cycles
- **디바이스**: GPU
- **배경색**: 짙은 블루-그레이 (0.05, 0.05, 0.08)

### 조명 설정
- **키 라이트**: 강도 1000, 전면 상단
- **필 라이트**: 강도 500, 측면 상단
- **백 라이트**: 강도 300, 후면 상단
- **앰비언트 라이트**: 강도 200, 중앙 상단

### 카메라 설정
- **위치**: (4, -4, 2.5)
- **회전**: (70°, 0°, 45°)
- **렌즈**: 50mm

## 커스터마이즈

### 신체 비율 조정
`create_humanoid_base()` 메서드에서 변수 수정:
```python
height = 1.8  # 전체 높이 (미터)
head_radius = 0.12  # 머리 반지름
torso_width = 0.4  # 상체 너비
# ... 기타 비율 변수
```

### 재질 수정
`setup_materials()` 메서드에서 색상 및 속성 수정:
```python
bsdf.inputs['Base Color'].default_value = (R, G, B, 1.0)
bsdf.inputs['Metallic'].default_value = 0.9
bsdf.inputs['Roughness'].default_value = 0.3
```

### 부품 추가/제거
각 생성 메서드에서 코드 추가/삭제:
- `create_humanoid_base()`: 기본 구조
- `create_internal_skeleton()`: 내골격
- `create_external_armor()`: 외골격
- `create_energy_cores()`: 에너지 코어
- `create_joints()`: 관절

## 문제 해결

### 스크립트 실행 오류
1. Blender 버전 확인 (4.4 이상 필요)
2. Python API 호환성 확인
3. 콘솔 로그에서 에러 메시지 확인

### 렌더링 문제
1. GPU 드라이버 업데이트
2. Cycles 디바이스를 CPU로 변경
3. 메모리 부족 시 샘플 수 감소

### 재질 표시 문제
1. 뷰포트 쉐이딩 모드를 'Material Preview'로 변경
2. 'Rendered' 모드에서 확인
3. 노드 연결 확인

## 팁

### 성능 최적화
- 복잡한 장면에서는 렌더 샘플 수 감소
- GPU 메모리 부족 시 타일 크기 조정
- 불필요한 오브젝트 숨기기

### 애니메이션 준비
- 생성된 오브젝트에 리깅 추가
- 아마추어 설정
- IK 제어 추가

### 내보내기
- `.blend` 파일로 저장
- FBX/OBJ 형식으로 내보내기
- 다른 3D 소프트웨어와 호환

## 추가 리소스

- [Blender 공식 문서](https://docs.blender.org/)
- [Blender Python API](https://docs.blender.org/api/current/)
- [Cycles 렌더링 가이드](https://docs.blender.org/manual/en/latest/render/cycles/)

## 저작권
- 작성자: 정구영
- 작성일: 2026년 05월 20일
- 프로젝트: Android Cyborg Transformers (ACTF)

# Python 환경변수 설정

## windows

일시적 환경변수 설정

    >set PYTHONPATH framework_dir

영구적 환경변수 설정

    >setx PYTHONPATH framework_dir

기존에 있던 환경변수에 추가

    >setx PYTHONPATH %PYTHONPATH%framework_dir

환경 변수 확인

    cmd
        >set PYTHONPATH
    powershell
        >$env:PYTHONPATH

## 코드상 추가

    import sys
    sys.path.append(framework_dir)

단, 코드를 통해서 추가하게되면 해당 프로세스 내에서만 추가되므로 프로세스 실행시 마다 추가가 필요
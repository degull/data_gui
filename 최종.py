import sys  # 시스템 모듈 임포트
# pyQt5 모듈에서 필요한 위젯 임포트
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLabel, QVBoxLayout, QWidget, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap # pyQt5 모듈에서 QPixmap 임포트
import pandas as pd # pandas 모듈을 임포트
import matplotlib.pyplot as plt # matplotlib 모듈에서 pyplot을 임포트
from PyQt5.QtWidgets import QHBoxLayout # PyQt5 모듈에서 QHBoxLayout을 임포트

from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas # matplotlib 모듈에서 FigureCanvas를 임포트
from matplotlib.figure import Figure    # matplotlib 모듈에서 Figure를 임포트

from PyQt5.QtCore import Qt # PyQt5 모듈에서 Qt를 임포트

# `MainWindow` 클래스는 `QMainWindow` 클래스를 상속받아 생성된 사용자 정의 클래스
#  pyQt5를 사용해 GUI 메인 창 구현하는 클래스
class MainWindow(QMainWindow):
    def __init__(self):     # `__init__` 메소드는 클래스의 생성자 함수로서, 객체가 생성될 때 호출
        super().__init__()  # `super().__init__()`은 부모 클래스인 `QMainWindow`의 생성자를 호출하여 부모 클래스의 기능을 초기화

        self.setWindowTitle("CSV GUI 구현")     # 윈도우 제목 설정
        self.setGeometry(200, 200, 800, 600)  # 윈도우 크기 조정

# 버튼, 텍스트 에디터, 레이블 등 위젯 생성

        # 버튼 및 텍스트 에디터 `QTextEdit` 위젯의 인스턴스를 생성하여 창에 추가 
        self.button = QPushButton("첨부하기", self)
        self.button.clicked.connect(self.load_file)
        self.text_edit = QTextEdit(self)
        self.label = QLabel(self)   # 레이블은 `QLabel` 위젯의 인스턴스를 생성하여 창에 추가
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)

        # 레이아웃 설정
        # 레이아웃은 `QVBoxLayout`을 사용하여 위젯들을 수직으로 배치하도록 설정
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.text_edit)

        # 입력 상자를 추가하는 레이아웃은 `QHBoxLayout`을 사용하여 수평으로 배치하도록 설정
        input_layout = QHBoxLayout()
        self.column_input = QLineEdit(self)
        self.column_input.returnPressed.connect(self.display_column)
        input_layout.addWidget(self.column_input)
        layout.addLayout(input_layout)

        # 이미지를 감싸는 레이아웃은 수평으로 배치되도록 `QHBoxLayout`을 사용하여 레이아웃을 설정
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.label)
        image_layout.addWidget(self.label1)
        image_layout.addWidget(self.label2)
        image_layout.addWidget(self.label3)
        layout.addLayout(image_layout)

        # 추가한 레이아웃을 메인 윈도우에 설정
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # `load_file` 메서드는 파일 선택 대화상자를 통해 CSV 파일을 선택하고,
    #  선택된 파일을 읽어와 데이터프레임으로 변환
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", "CSV 파일 (*.csv)")

        if file_path:
            # CSV 파일 불러오기
            try:
                self.df = pd.read_csv(file_path)    # 선택된 파일이 있으면 데이터프레임의 내용을 텍스트 에디터에 표시
                self.df1 = pd.read_csv(file_path)
                # CSV 파일 내용 출력
                self.text_edit.setPlainText(self.df.to_string())

                self.graphs(self.df) # 직선 그래프
                # 그래프를 이미지 파일로 저장
                image_path = "graph_image.png"
                plt.savefig(image_path)
                # 이미지 출력
                self.set_image(image_path,0)

                self.scatter(self.df) # 산점도
                image_path = "graph_image.png"
                plt.savefig(image_path)
                self.set_image(image_path,1)

                self.barchart(self.df) # 막대 그래프
                image_path = "graph_image2.png"
                plt.savefig(image_path)
                self.set_image(image_path,2)
                
                self.piechart(self.df1) # 파이 그래프
                image_path = "graph_image.png"
                plt.savefig(image_path)
                self.set_image(image_path,3)
                

            except pd.errors.ParserError:
                self.text_edit.setPlainText("잘못된 파일 형식입니다.")

    # 각 함수는 데이터프레임을 기반으로 그래프를 생성하고, 그래프의 타이틀, 축 레이블 등 설정

    
    # 여러개
    def graphs(self, df):
        # 데이터프레임의 열 개수 계산
        cols = len(df.columns) - 1

        # # 'Axis [nm]' 열의 값에서 특정 문자를 제거하고 숫자로 변환
        df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
        x = df['Axis [nm]']
        
        # 새로운 그래프 창 생성
        plt.figure()
        
        # 열 개수만큼 반복하면서 그래프 생성
        for i in range(1, cols+1):
            colName = f'ROI {i} []' # 열 이름 지정
            # 열의 값에서 특정 문자 제거하고 숫자로 변환
            df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
            y = df[colName]
             
            plt.plot(x, y, label=colName)   # 그래프 생성
            # plt.tight_layout()
            # 범례 추가
            plt.legend(loc='lower left', bbox_to_anchor=(1.0,0.0), frameon=True)
        
        # 그래프 제목 설정
        plt.title('Graph of ROIs')

        # x축, y축 레이블 설정
        plt.xlabel('Axis [nm]')
        plt.ylabel('Intensity')
        plt.tight_layout()  # 그래프 요소들을 자동으로 조절하여 균형있게 배치
        
    # 산점도 그래프
    def scatter(self, df):
        # 데이터프레임의 열 개수 계산
        cols = len(df.columns) - 1
        
        # 'Axis [nm]' 열의 값에서 특정 문자를 제거하고 숫자로 변환해 x축 값으로 사용하기 위해 처리
        df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
        x = df['Axis [nm]']
    
        # 새로운 그래프 창 생성
        plt.figure()
        
        # 열 개수만큼 반복하면서 산점도 그래프 생성(1부터 열 개수까지 반복)
        for i in range(1, cols+1):
            colName = f'ROI {i} []'     # 열 이름 지정
            # 열의 값에서 특정 문자 제거하고 숫자로 변환해 y축 값으로 사용하기 위해 처리
            df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
            y = df[colName]
            
            plt.scatter(x, y, label=colName)   # x축과 y축 데이터를 전달하여 산점도 그래프를 생성하는 함수
            
            # 범례 추가
            # loc 매개변수로 범례의 위치를 지정
            # bbox_to_anchor 매개변수로 범례의 상대적인 위치 지정
            plt.legend(loc='lower left', bbox_to_anchor=(1.0,0.0), frameon=True)

        # 그래프 제목 설정
        plt.title('Graph of ROIs')

        # x축, y축 레이블 설정
        plt.xlabel('Axis [nm]')
        plt.ylabel('Intensity')
        plt.tight_layout()  # 그래프 요소들을 자동으로 조절하여 균형있게 배치
        
    # 막대 차트
    def barchart(self, df):
        colName = 'ROI 1 []' # 사용할 열 이름 지정
        
        # 'Axis [nm]' 열의 값에서 특정 문자 제거하고 숫자로 변환
        df['Axis [nm]'] = df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
        x = df['Axis [nm]']
        
        # 선택한 열의 값에서 특정 문자 제거하고 숫자로 변환
        df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(float)
        y = df[colName]
        
        plt.figure()
        plt.bar(x, y)   # 막대 차트 생성
        plt.xlabel(df.columns[1])   # x축 레이블 설정
        plt.ylabel(df.columns[0])   # y축 레이블 설정
        plt.axis([860, 975, 0, 55]) # x축과 y축의 범위 설정
        plt.title(colName + " " + 'Axis')   # 그래프 제목 설정
    
    # 원 그래프
    def piechart(self,df):
        colName = 'ROI 1 []'    # 사용할 열 이름 지정
        # 선택한 열의 값에서 특정 문자 제거하고 정수로 변환
        df[colName] = df[colName].replace('[\$,]', '', regex=True).astype(int)
        df[colName] = round(df[colName].div(10,1))
        
        data = []

        for i in range(1,6):
            # 각 범위에 해당하는 데이터의 비율 계산
            data.append(len(df.loc[df[colName] == i])/len(df[colName]))
        
        plt.figure()
        y = pd.DataFrame(data)
         # 파이 차트 생성
        y.plot.pie(subplots=True,labels=['10-19','20-29','30-39','40-49','50-59'],autopct='%.1f')
        plt.legend(loc='lower left', bbox_to_anchor=(1.0,0.0),frameon=True)  # 범례 추가
        plt.title(colName)  # 그래프 제목 설정
    
    # 선 한개
    def oneGraph(self,column_name):
        # 'Axis [nm]' 열의 값에서 특정 문자 제거하고 숫자로 변환
        self.df['Axis [nm]'] = self.df['Axis [nm]'].replace('[\$,]', '', regex=True).astype(float)
        x = self.df['Axis [nm]']

        # 선택한 열의 값에서 특정 문자 제거하고 숫자로 변환
        self.df[column_name] = self.df[column_name].replace('[\$,]', '', regex=True).astype(float)
        y = self.df[column_name]
         
        plt.figure()
        plt.plot(x,y)   # 선 그래프 생성
        plt.axis([860,975,0,55])    # x축과 y축의 범위 설정
        plt.title(column_name+" "+'Axis')   # 그래프 제목 설정
        plt.xlabel('Axis [nm]') # x축 레이블 설정
        plt.ylabel('Intensity') # y축 레이블 설정

    # `set_text` 메서드는 텍스트 에디터에 텍스트를 설정하는 함수
    def set_text(self, text):
        self.text_edit.setPlainText(text)

    # `set_image` 메서드는 이미지 파일을 레이블에 표시하는 함수
    # 이미지 파일 경로를 인수로 받아 해당 이미지를 `QPixmap`으로 변환
    def set_image(self, image_path, num_label):
        pixmap = QPixmap(image_path)
        
        # num_label에 따라 해당하는 라벨 위젯에 이미지 설정
        # 가로 크기를 400으로 조정
        if num_label == 0: 
            self.label.setPixmap(pixmap.scaledToWidth(400))  
        elif num_label == 1:
            self.label1.setPixmap(pixmap.scaledToWidth(400))  
        elif num_label == 2:
            self.label2.setPixmap(pixmap.scaledToWidth(400)) 
        elif num_label == 3:
            self.label3.setPixmap(pixmap.scaledToWidth(400))  

    # display_column 함수는 컬럼을 표시하는 함수
    def display_column(self):
        column_name = self.column_input.text()
        if column_name in self.df.columns:  # 입력받은 column_name이 데이터프레임의 컬럼들 중에 존재한다면 해당 컬럼을 column 변수에 저장
            column = self.df[column_name]
            
            # self.text_edit 위젯에 column을 문자열 형태로 설정하여 표시
            self.text_edit.setPlainText(column.to_string())
            
            # `oneGraph` 메서드는 주어진 열 이름을 기반으로 단일 선 그래프를 생성
            # 주어진 열의 데이터를 추출하여 그래프를 생성하고, 그래프의 타이틀, 축 레이블 등을 설정
            self.oneGraph(column_name)
            image_path = "graph_image.png"  # 그래프를 이미지 파일로 저장하고, 그래프 이미지를 라벨 위젯에 출력
            plt.savefig(image_path)
            # 이미지 출력
            self.set_image(image_path,0)
            
            # 만약 입력받은 column_name이 데이터프레임의 컬럼들 중에 존재하지 않는다면
            #  "Invalid column name."을 self.text_edit 위젯에 표시
        else:
            self.text_edit.setPlainText("Invalid column name.")


if __name__ == "__main__":
    app = QApplication(sys.argv)    # QApplication 객체를 생성하여 애플리케이션을 초기화
    window = MainWindow()   # MainWindow 객체를 생성하고 화면에 표시
    window.show()
    sys.exit(app.exec_())
    

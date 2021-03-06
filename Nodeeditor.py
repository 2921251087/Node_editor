#!/usr/bin/python
# -*-coding:utf-8 -*-
u"""
@创建时间
    2020/9/1 11:45
@作者
    苍之幻灵
@我的主页
    http://www.cpcgskill.com
@QQ
    2921251087
@爱发电
    https://afdian.net/@Phantom_of_the_Cang
@aboutcg
    https://www.aboutcg.org/teacher/54335
@bilibili
    https://space.bilibili.com/351598127
"""
import sys

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    try:
        from PySide2.QtGui import *
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
    except ImportError:
        try:
            from PySide.QtGui import *
            from PySide.QtCore import *
            from PySide.QtWidgets import *
        except:
            print('ImportError')

DEBUG = True



class NodeView(QWidget):
    DEF, ADD, REMOVE = range(3)
    SEL, SELED, MOVE = range(3)

    def __init__(self, parent = None):
        super(NodeView, self).__init__(parent)
        self.setMouseTracking(True)
        # 场景位置
        self._scenes_pos = QPoint(10, 10)
        # 场景缩放
        self._scenes_zoom = 0.5
        # 场景大小
        self._scenes_size = 10000

        # 节点列表
        self._nodes = list()
        # 节点名称 | 对象字典
        self._node_name_dict = dict()
        # 选择的节点列表
        self._select_nodes = list()
        # 选择状态
        self._select_status = self.DEF
        # 选择操作的状态
        self._set_select_status = self.SEL
        # 框选开始点
        self._select_rect_start_pt = None
        # 框选结束点
        self._select_rect_end_pt = None

        # 鼠标左键按下
        self._l_bn_dw = False
        # 鼠标中键按下
        self._m_bn_dw = False

        # shift按下
        self._shift_dw = False
        # ctr按下
        self._ctr_dw = False

        # 移动场景时的上一个点
        self._up_pos = QPoint(0, 0)

        # 场景路径
        self._scenes_path = self.initScenesPath()

        # 属性连接列表
        self._attr_connect = list()

    def removeAllSelect(self):
        u"""
        清空所有节点的选择

        :return:
        """
        for i in self._select_nodes:
            i.is_select = False
            i.is_select_end = False

        self._select_nodes = list()

    def select(self, *args):
        u"""
        选择节点

        :param args:
        :return:
        """
        for i in self._select_nodes:
            i.is_select = False
            i.is_select_end = False
        if self._select_status == self.DEF:
            self._select_nodes = list()
            for obj in args:
                self._select_nodes.append(obj)
        elif self._select_status == self.ADD:
            for obj in args:
                while True:
                    if obj in self._select_nodes:
                        self._select_nodes.remove(obj)
                    else:
                        break
                self._select_nodes.append(obj)

        else:
            for obj in args:
                while True:
                    if obj in self._select_nodes:
                        self._select_nodes.remove(obj)
                    else:
                        break
        for i in self._select_nodes:
            i.is_select = True
        if len(self._select_nodes):
            self._select_nodes[-1].is_select_end = True

    def addNode(self, node):
        u"""
        添加节点

        :param node:
        :return:
        """
        self._nodes.append(node)
        self._node_name_dict[node._data[u"name"]] = node

    def removeNode(self, node):
        u"""
        移除节点

        :param node:
        :return:
        """
        if node in self._nodes:
            self._nodes.remove(node)
        if node._data[u"name"] in self._node_name_dict:
            self._nodes.pop(node._data[u"name"])
    def connect(self, out_attr = "", in_attr = ""):
        out_attr_sp = out_attr.split(".")
        if len(out_attr_sp) != 2:
            return
        in_attr_sp = in_attr.split(".")
        if len(in_attr_sp) != 2:
            return
        # xxx.xxx
        if not out_attr_sp[0] in self._node_name_dict:
            return
        if not in_attr_sp[0] in self._node_name_dict:
            return
        out_node = self._node_name_dict[out_attr_sp[0]]
        in_node = self._node_name_dict[in_attr_sp[0]]

    def initScenesPath(self):
        u"""
        初始化场景路径

        :return:
        """
        path = QPainterPath()
        _lines = list()
        _range = list(range(-self._scenes_size, self._scenes_size + 1, 100))

        # 绘制背景线
        for i in _range:
            # 横向线
            path.moveTo(QPoint(-self._scenes_size, i))
            path.lineTo(QPoint(self._scenes_size, i))
            # 竖向线
            path.moveTo(QPoint(i, -self._scenes_size))
            path.lineTo(QPoint(i, self._scenes_size))
        return path

    def scaleScenes(self, scale = 1.0):
        u"""
        场景缩放方法

        :param scale:
        :return:
        """
        self._scenes_zoom = min(max(self._scenes_zoom * scale, 0.25), 1)

    def drawBackground(self, p = QPainter, rect = QRect):
        u"""
        绘制背景

        :param rect:
        :return:
        """
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(60, 63, 65)))
        p.drawRect(rect)

    def drawScenes(self, p = QPainter, rect = QRect):
        u"""
        绘制场景

        :param p:
        :param rect:
        :return:
        """

        p.setPen(QPen(QColor(53, 53, 53), 2))
        p.drawPath(self._scenes_path)
        # 绘制定位
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(255, 255, 255, 20)))
        p.drawRect(QRect(0, 0, 50, 50))

        p.setPen(QPen(QColor(255, 0, 0), 5))
        p.drawLine(QLine(QPoint(0, 0), QPoint(self._scenes_size, 0)))
        p.setPen(QPen(QColor(0, 255, 0), 5))
        p.drawLine(QLine(QPoint(0, 0), QPoint(0, self._scenes_size)))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(255, 255, 255)))
        p.drawEllipse(QPoint(0, 0), 5, 5)

    def drawDebug(self, p = QPainter, rect = QRect):
        p.drawText(QPoint(10, 20), u"视图坐标" + str(self._scenes_pos))
        p.drawText(QPoint(10, 40), u"视图缩放 ：" + str(self._scenes_zoom))

    def mapToView(self, pos = QPoint):
        u"""
        将屏幕坐标系转化为视图坐标系

        :param pos:
        :return:
        """
        return (pos - self._scenes_pos) * (1.0 / self._scenes_zoom)

    def mousePressEvent(self, event = QMouseEvent):
        u"""
        鼠标按下事件

        :param event:
        :return:
        """
        pos = QCursor.pos()
        self._up_pos = pos
        if event.button() == Qt.LeftButton:
            self._l_bn_dw = True
        if event.button() == Qt.MidButton:
            self._m_bn_dw = True
        elif event.button() == Qt.LeftButton:
            self._set_select_status = self.SEL
            view_pos = self.mapToView(self.mapFromGlobal(pos))
            for i in reversed(self._nodes):
                rect = i.rect()
                node_pos = i.pos
                rect = QRect(rect.x() + node_pos.x(), rect.y() + node_pos.y(), rect.width(), rect.height())
                if rect.contains(view_pos):
                    if not i.is_select:
                        self._set_select_status = self.SELED
                        self.select(i)
                    break
            else:
                self._select_rect_start_pt = view_pos
        self.update()

    def mouseMoveEvent(self, event = QMoveEvent):
        u"""
        鼠标移动事件

        :param event:
        :return:
        """
        pos = QCursor.pos()

        view_pos = (self.mapFromGlobal(pos) - self._scenes_pos) * (1.0 / self._scenes_zoom)
        for i in reversed(self._nodes):
            rect = i.rect()
            node_pos = i.pos
            rect = QRect(rect.x() + node_pos.x(),
                         rect.y() + node_pos.y(),
                         rect.width(),
                         rect.height())
            if rect.contains(view_pos):
                i.is_the_mouse_inside = True
            else:
                i.is_the_mouse_inside = False

            for t in i._attr_objects:
                attr_rect = t.rect()
                attr_pos = t.pos
                attr_rect = QRect(rect.x() + attr_rect.x() + attr_pos.x(),
                                  rect.y() + attr_rect.y() + attr_pos.y(),
                                  attr_rect.width(),
                                  attr_rect.height())
                if attr_rect.contains(view_pos):
                    t.is_the_mouse_inside = True
                else:
                    t.is_the_mouse_inside = False

        if self._m_bn_dw:
            self._scenes_pos += (pos - self._up_pos)
        elif self._l_bn_dw:
            self._set_select_status = self.MOVE
            if self._select_rect_start_pt:
                self._select_rect_end_pt = self.mapToView(self.mapFromGlobal(pos))
            else:
                # 移动选择的节点
                for i in self._select_nodes:
                    i.pos = i.pos + (pos - self._up_pos) / self._scenes_zoom
        self._up_pos = pos
        self.update()

    def mouseReleaseEvent(self, event = QMouseEvent):
        u"""
        鼠标提起事件

        :param event:
        :return:
        """
        if self._l_bn_dw:
            if self._set_select_status == self.SELED:
                pass
            elif self._set_select_status == self.SEL:
                view_pos = (self.mapFromGlobal(QCursor.pos()) - self._scenes_pos) * (1.0 / self._scenes_zoom)
                for i in reversed(self._nodes):
                    rect = i.rect()
                    node_pos = i.pos
                    rect = QRect(rect.x() + node_pos.x(), rect.y() + node_pos.y(), rect.width(), rect.height())
                    if rect.contains(view_pos):
                        self.select(i)
                        break
                else:
                    self.removeAllSelect()
            else:
                if self._select_rect_start_pt and self._select_rect_end_pt:
                    objs = list()
                    r = QRect(self._select_rect_start_pt, self._select_rect_end_pt)
                    for i in reversed(self._nodes):
                        rect = i.rect()
                        node_pos = i.pos
                        rect = QRect(rect.x() + node_pos.x(), rect.y() + node_pos.y(), rect.width(), rect.height())
                        if rect.intersects(r):
                            objs.append(i)
                    objs.sort(key = lambda i:(i.pos - self._select_rect_start_pt).manhattanLength())
                    self.select(*objs)
            self._select_rect_start_pt = None
            self._select_rect_end_pt = None
        if event.button() == Qt.MidButton:
            self._m_bn_dw = False
        if event.button() == Qt.LeftButton:
            self._l_bn_dw = False
        self.update()

    def wheelEvent(self, event = QWheelEvent):
        u"""
        滚轮旋转事件

        :param event:
        :return:
        """
        if event.angleDelta().y() > 0 or event.angleDelta().x() > 0:
            pos = (self.mapFromGlobal(QCursor.pos()) - self._scenes_pos) * (1.0 / self._scenes_zoom)
            self.scaleScenes(1.25)
            self._scenes_pos -= (pos * self._scenes_zoom + self._scenes_pos) - self.mapFromGlobal(QCursor.pos())
            self.update()
        else:
            pos = (self.mapFromGlobal(QCursor.pos()) - self._scenes_pos) * (1.0 / self._scenes_zoom)
            self.scaleScenes(0.8)
            self._scenes_pos -= (pos * self._scenes_zoom + self._scenes_pos) - self.mapFromGlobal(QCursor.pos())
            self.update()

    def keyPressEvent(self, event = QKeyEvent):
        u"""
        键盘按下事件

        :param event:
        :return:
        """
        # shift
        if event.modifiers() == Qt.ShiftModifier:
            self._shift_dw = True
            self._select_status = self.ADD
        # ctr
        if event.modifiers() == Qt.ControlModifier:
            self._ctr_dw = True
            self._select_status = self.REMOVE

    def keyReleaseEvent(self, event = QKeyEvent):
        u"""
        按键提起事件
        :param event:
        :return:
        """
        self._shift_dw = False
        self._ctr_dw = False
        self._select_status = self.DEF

    def paintEvent(self, event = QPaintEvent):
        u"""
        绘图事件

        :param event:
        :return:
        """
        rect = self.rect()

        # 绘制背景
        p = QPainter(self)
        self.drawBackground(p, rect)
        p.end()

        # 绘制场景
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        # 场景矩阵
        p.translate(self._scenes_pos.x(), self._scenes_pos.y())
        p.scale(self._scenes_zoom, self._scenes_zoom)
        self.drawScenes(p, rect)
        p.setPen(Qt.NoPen)
        p.setBrush(Qt.NoBrush)
        for i in self._nodes:
            i._painter(p)
        # 绘制选择框
        if self._select_rect_start_pt and self._select_rect_end_pt:
            r = QRect(self._select_rect_start_pt, self._select_rect_end_pt)
            p.setPen(Qt.NoPen)
            p.setBrush(QBrush(QColor(255, 255, 255, 10)))
            p.drawRect(r)
        p.end()

        if DEBUG:
            p = QPainter(self)
            self.drawDebug(p, rect)
            p.end()



AttrDataMode = {
    u"name":u"Test",
    u"Type":u"*"
    }
dataMode = {
    u"name":u"xxx",
    u"in_attr":[AttrDataMode, AttrDataMode],
    u"out_attr":[AttrDataMode, AttrDataMode, AttrDataMode]
    }
node1 = {
    u"name":u"xxx",
    u"in_attr":[AttrDataMode],
    u"out_attr":[AttrDataMode]
    }
node2 = {
    u"name":u"xxx",
    u"in_attr":[AttrDataMode],
    u"out_attr":[AttrDataMode]
    }

class NodeBase(object):
    pos = QPoint(0, 0)
    # 鼠标是否在内部
    is_the_mouse_inside = False
    # 是否被选择
    is_select = False
    # 是否为最后一个选择节点
    is_select_end = False

    def __init__(self, data = dataMode):
        self._data = data
        self._inattr_objects = list()
        self._outattr_objects = list()

    def rect(self):
        pass

    def addInAttr(self, obj):
        self._inattr_objects.append(obj)
    def addOutAttr(self, obj):
        self._outattr_objects.append(obj)
    def _painter(self, p = QPainter):
        tr = p.transform()
        p.translate(self.pos)
        self.painter(p)
        for i in self._attr_objects:
            i._painter(p)
        p.setTransform(tr)

    def painter(self, p = QPainter):
        pass



class AttrBase(object):
    pos = QPoint(0, 0)
    # 鼠标是否在内部
    is_the_mouse_inside = False

    def __init__(self, data = AttrDataMode):
        self._data = data
        self._attr_objects = list()

    def rect(self):
        pass

    def _painter(self, p = QPainter):
        tr = p.transform()
        p.translate(self.pos)
        self.painter(p)
        p.setTransform(tr)

    def painter(self, p = QPainter):
        pass



class TestNode(NodeBase):
    name_font = QFont("微软雅黑", 40, QFont.Bold)

    def __init__(self, data = dataMode):
        super(TestNode, self).__init__(data)
        self._rect = QRect(0, 0, 250, 80)

        in_attr_size = len(self._data[u"in_attr"]) - 1
        for ID, i in enumerate(self._data[u"in_attr"]):
            o = TestAttr(i)
            try:
                o.pos = QPoint(50 + float(ID) / in_attr_size * 150, -20)
            except ZeroDivisionError:
                o.pos = QPoint(125, -20)
            self.addAttr(o)


        out_attr_size = len(self._data[u"out_attr"]) - 1
        for ID, i in enumerate(self._data[u"out_attr"]):
            o = TestAttr(i)
            try:
                o.pos = QPoint(50 + float(ID) / out_attr_size * 150, 100)
            except ZeroDivisionError:
                o.pos = QPoint(125, 100)
            self.addAttr(o)

    def rect(self):
        return self._rect

    def painter(self, p = QPainter):
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(0, 0, 0, 75)))
        p.drawRoundedRect(self._rect.adjusted(6, 6, 6, 6), 25, 25)

        if self.is_select_end:
            p.setPen(QPen(QColor(10, 255, 10), 5))
        elif self.is_select:
            p.setPen(QPen(QColor(125, 125, 125), 5))
        elif self.is_the_mouse_inside:
            p.setPen(QPen(QColor(255, 255, 10), 5))
        else:
            p.setPen(QPen(QColor(0, 0, 0), 3))
        p.setBrush(QBrush(QColor(252, 252, 252)))
        p.drawRoundedRect(self._rect, 25, 25)

        p.setPen(QPen(QColor(0, 0, 0), 5))
        p.setFont(self.name_font)
        p.drawText(QPoint(10, 55), self._data[u"name"])



class TestAttr(AttrBase):
    def __init__(self, data = AttrDataMode):
        super(TestAttr, self).__init__(data)
        self._rect = QRect(-10, -10, 20, 20)

    def rect(self):
        return self._rect

    def painter(self, p = QPainter):
        if self.is_the_mouse_inside:
            p.setPen(QPen(QColor(255, 255, 10), 5))
        else:
            p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(255, 255, 255)))
        # p.drawEllipse(self._rect)
        p.drawRect(self._rect)




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = NodeView()
    n = TestNode(data=node1)
    win.addNode(n)
    n = TestNode(data=node2)
    n.pos = QPoint(100, 100)
    win.addNode(n)

    win.show()
    sys.exit(app.exec_())

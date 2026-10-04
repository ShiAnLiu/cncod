    # ---------- 表达式翻译 ----------
    def 表达式(self, 节):
        t = 节.类型
        if t in ('数', '文本'):
            return repr(节.值)
        if t == '真': return 'True'
        if t == '假': return 'False'
        if t == '列表':
            return '[' + ', '.join(self.表达式(x) for x in 节.元素) + ']'
        if t == '名':
            self.查名(节.名字, 节.行)
            return 节.名字
        if t == '负':
            return f'-{self.表达式(节.值)}'
        if t == '非':
            return f'not {self.表达式(节.值)}'
        if t == '逻辑':
            运算 = 'and' if 节.运算 == '并且' else 'or'
            return f'bool({self.表达式(节.左)} {运算} {self.表达式(节.右)})'
        if t == '访问':
            return f'{self.表达式(节.对象)}.{节.成员}'
        if t == '运算':
            左, 右 = self.表达式(节.左), self.表达式(节.右)
            if 节.运算 == '加':
                return f'_加({左}, {右})'
            if 节.运算 in self._比较运算:
                return f'{左} {self._比较运算[节.运算]} {右}'
            return f'{左} {self._算术运算[节.运算]} {右}'
        if t == '调用':
            被调 = 节.被调
            实参串 = ', '.join(self.表达式(a) for a in 节.实参)
            if 被调.类型 == '名' and 被调.名字 in _内置函数名:
                return f'_{被调.名字}({实参串})'
            return f'{self.表达式(被调)}({实参串})'
        raise 华语编译错误(f'无法编译的表达式「{t}」', 节.行)

from grammarize.grammarize import Gree


t0 = Gree('body',
          Gree('div'),
          Gree('div'))

t1 = Gree('body',
          Gree('div'),
          Gree('div', Gree('wat',
                           Gree('duh'),
                           Gree('eww'))))

t2 = Gree('body',
          Gree('ldiv'),
          Gree('rdiv',
               Gree('lwat',
                    Gree('lduh'),
                    Gree('leww')),
               Gree('rwat',
                    Gree('rduh'),
                    Gree('reww'))))

t3 = Gree('body',
          Gree('pre'),
          Gree('div',
               Gree('p',
                    Gree('h1'),
                    Gree('span')),
               Gree('p',
                    Gree('h2'),
                    Gree('a'))))

g3 = Gree('body',
          Gree('pre'),
          Gree('div',
               Gree('p',
                    Gree('h1'),
                    Gree('span')),
               Gree('p',
                    Gree('h2'),
                    Gree('a'))))

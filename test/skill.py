from app.skill.skill import Projectile


def test_projectile():
    p = Projectile([0, 0], [6, 5])
    r = p.get_accel([6, 5])
    for _ in p:
        if p.pos[0] > 8 or p.pos[1] > 8:
            break
        print(_)

test_projectile()

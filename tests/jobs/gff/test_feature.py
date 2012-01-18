from nose.tools import eq_, ok_

from jobs.gff.feature import Feature



def test_Feature():
    a = '\t'.join(['Chr1', 'TAIR10', 'gene', '2', '20', '.', '+', 
                   '.', 'ID=Gene1;Parent=p'])
    f = Feature.from_string(a)
    eq_('Gene1', f.ID)
    eq_(['p'], f.parents)

    b = '\t'.join(['Chr1', 'TAIR10', 'gene', '2', '20', '.', '+', 
                   '.', 'ID=Gene1;Parent=p,q'])
    f = Feature.from_string(b)
    eq_(['p', 'q'], f.parents)

    c = '\t'.join(['Chr1', 'TAIR10', 'gene', '2', '20', '.', '+', 
                   '.', ''])
    f = Feature.from_string(c)
    eq_('', f.ID)
    eq_([], f.parents)

import pytest
import torch
from complexityrouter import ComplexityRouter, create_complexityrouter

class TestComplexityRouter:
    def test_init(self):
        m = ComplexityRouter(dim=256, hidden_dim=512)
        assert m.dim == 256
    
    def test_forward(self):
        m = ComplexityRouter(dim=256)
        x = torch.randn(32, 256)
        assert m(x).shape == (32, 256)
    
    def test_factory(self):
        m = create_complexityrouter()
        assert isinstance(m, ComplexityRouter)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

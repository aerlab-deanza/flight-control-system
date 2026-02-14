# Contributing Guide

## Workflow

1. **Create a branch** for your feature
```bash
   git checkout -b feature/plant-physics
```

2. **Make your changes**
   - Write code
   - Add tests
   - Update README if needed

3. **Test locally**
```bash
   pytest  # For simulator
   # Or build + test firmware
```

4. **Commit with clear message**
```bash
   git commit -m "Add plant physics with torque saturation

   - Implements 1-axis rotational dynamics
   - Includes Euler integration
   - Adds test script
   - Fixes #2
   "
```

5. **Push and create PR**
```bash
   git push origin feature/plant-physics
   # Create Pull Request on GitHub
```

6. **Code review**
   - At least one team member reviews
   - Address feedback
   - Merge when approved

## Code Standards

**Python (Simulator):**
- Follow PEP 8
- Use type hints where helpful
- Docstrings for classes and functions
- Keep functions < 50 lines

**C++ (Firmware):**
- Follow Google C++ style
- Comment non-obvious logic
- Use const where appropriate
- Keep ISR functions fast (< 100 μs)

## Testing

- Write tests for critical functions
- Run `pytest` before committing simulator code
- Bench test firmware before flight tests

## Documentation

- Update README when adding features
- Document interfaces between modules
- Add comments for complex math
- Keep docs/ up to date

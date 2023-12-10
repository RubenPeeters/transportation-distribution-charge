Output of benchmarking:

```bash
Execution with variables m=1 d=1 took 0.007911s
Execution with variables m=1 d=7 took 0.007094s
Execution with variables m=1 d=31 took 0.006161s
Execution with variables m=1 d=365 took 0.006289s
Execution with variables m=1 d=730 took 0.005704s
Execution with variables m=1 d=3652 took 0.005141s
Execution with variables m=10 d=1 took 0.006888s
Execution with variables m=10 d=7 took 0.006026s
Execution with variables m=10 d=31 took 0.006110s
Execution with variables m=10 d=365 took 0.005745s
Execution with variables m=10 d=730 took 0.005724s
Execution with variables m=10 d=3652 took 0.005517s
Execution with variables m=100 d=1 took 0.011081s
Execution with variables m=100 d=7 took 0.011187s
Execution with variables m=100 d=31 took 0.011267s
Execution with variables m=100 d=365 took 0.010716s
Execution with variables m=100 d=730 took 0.011770s
Execution with variables m=100 d=3652 took 0.011021s
Execution with variables m=1000 d=1 took 0.056621s
Execution with variables m=1000 d=7 took 0.056157s
Execution with variables m=1000 d=31 took 0.058849s
Execution with variables m=1000 d=365 took 0.057104s
Execution with variables m=1000 d=730 took 0.062417s
Execution with variables m=1000 d=3652 took 0.062443s
Execution with variables m=10000 d=1 took 0.444738s
Execution with variables m=10000 d=7 took 0.432227s
Execution with variables m=10000 d=31 took 0.464725s
Execution with variables m=10000 d=365 took 0.440904s
Execution with variables m=10000 d=730 took 0.429717s
Execution with variables m=10000 d=3652 took 0.430876s
Execution with variables m=100000 d=1 took 5.521942s
Execution with variables m=100000 d=7 took 5.812059s
Execution with variables m=100000 d=31 took 5.814914s
Execution with variables m=100000 d=365 took 5.776277s
Execution with variables m=100000 d=730 took 6.375355s
Execution with variables m=100000 d=3652 took 6.055677s
```

From the output we can tell that the `duration` does not have a significant impact on the execution time, meaning we have O(1) time complexity, referring to the `duration` input (`d`). The `amount of meters` however, does have a significant impact. We can intuitively see from the output that when the amount of meters increases tenfold, the execution time also increases (around) tenfold. This means we have O(n) time complexity, referring to the `amount of meters` input (`m`).

Improvements to the execution time:
If I look at my calculation steps, I realise that the two merges will likely take the most time, as the other calculations are vectorized and should be highly efficient. Another option is to calculate data based on lookups in the other tables. In the end this will probably also entail some merges, although they may be smaller. Intuitively, I think this will actually decrease the efficiency, hence why I chose the current implementation. Plus this makes the code (in my opinion) more complex to understand.  

Some improvements that can be made to the memory aspects is transforming the `exit_zone` parameter to categorical. This will reduce the memory it uses, as a variable of type `object` is free text, meaning the memory allocated has to be large, to be able to fit all possible inputs. When transforming to a categorical, we already know what the possible inputs will be, and do not have to allocate as much memory. This leads into a second problem we can have with a larger dataset. Memory issues. When the dataset becomes too large, it is possible that the dataset will no longer fit in memory, meaning we cannot perform vectorized operations on the entire dataset. This is annoying, but can be resolved with `chunking`, as it is called in pandas. We can also use efficient data storage options such as parquet to reduce loading times. 
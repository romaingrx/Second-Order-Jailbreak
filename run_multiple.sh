# Run multiple times the same program with two parameters
# Usage: ./run_multiple.sh <parameter1> <parameter2> <number of times>
# Example: ./run_multiple.sh envs/2-agents-simple-3v4-mistral.json --num_step 20 --num_run 10

if [ $# -ne 3 ]; then
    echo "Usage: ./run_multiple.sh <parameter1> <parameter2> <number of times>"
    exit 1
fi

for i in $(seq 1 $3); do
    echo "Run $i"
    python3 run_twoplayer.py $1 --num_step $2
done

echo "Done"


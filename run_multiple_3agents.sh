if [ $# -ne 3 ]; then
    echo "Usage: ./run_multiple_3agent.sh <parameter1> <parameter2> <number of times>"
    exit 1
fi

for i in $(seq 1 $3); do
    echo "Run $i"
    python3 run_intermediary.py $1 --num_step $2
done

echo "Done"


from flask import Flask, jsonify
from hdfs import InsecureClient

app = Flask(__name__)
hdfs_client = InsecureClient('http://localhost:9870', user='hadoop')

@app.route('/api/recommend/<int:movie_id>', methods=['GET'])
def recommend(movie_id):
    try:
        hdfs_path = '/output/part-00000'
        recommendations = []

        with hdfs_client.read(hdfs_path) as reader:
            movie_tags = {}  
            for line in reader:
                movie, tag_tf_idf = line.decode('utf-8').strip().split('\t')
                tag, tf_idf = tag_tf_idf.split(':')
                tf_idf = float(tf_idf)

                if int(movie) == movie_id:
                    movie_tags[tag] = tf_idf

            with hdfs_client.read(hdfs_path) as reader:
                for line in reader:
                    other_movie, tag_tf_idf = line.decode('utf-8').strip().split('\t')
                    tag, tf_idf = tag_tf_idf.split(':')
                    tf_idf = float(tf_idf)

                    if tag in movie_tags and int(other_movie) != movie_id:
                        similarity = movie_tags[tag] * tf_idf
                        recommendations.append((other_movie, similarity))

        recommendations = sorted(recommendations, key=lambda x: -x[1])[:5]
        return jsonify({"movie_id": movie_id, "recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

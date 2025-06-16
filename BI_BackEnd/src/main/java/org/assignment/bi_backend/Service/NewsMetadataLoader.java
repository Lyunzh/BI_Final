package org.assignment.bi_backend.Service;

import org.assignment.bi_backend.Entity.NewsMetadata;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

@Component
public class NewsMetadataLoader {
    private static final Map<String, NewsMetadata> metadataMap = new HashMap<>();

    @Value("${news.file.path}")
    private String path;

    @Autowired
    private ResourceLoader resourceLoader;

    @PostConstruct
    public void load() {
        Resource resource = resourceLoader.getResource(path);
        if (!resource.exists() || !resource.isReadable()) {
            throw new IllegalStateException("新闻元数据文件不存在或不可读: " + path);
        }

        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(resource.getInputStream(), StandardCharsets.UTF_8))) {
            String header = br.readLine();
            if (header == null) {
                throw new IllegalStateException("新闻元数据文件为空: " + path);
            }

            String line;
            int lineNum = 1;
            while ((line = br.readLine()) != null) {
                lineNum++;
                if (line.trim().isEmpty()) {
                    // 跳过空行
                    continue;
                }

                String[] parts = line.split("\t");
                try {
                    // Expect columns: News ID, Category, Topic, Headline, News body
                    if (parts.length < 5) continue;
                    String newsId = parts[0].trim();
                    String category = parts[1].trim();
                    String topic = parts[2].trim();
                    String headline = parts[3].trim();
                    String content = parts[4].trim();

                    NewsMetadata m = new NewsMetadata();
                    m.setNewsId(newsId);
                    m.setCategory(category);
                    m.setTopic(topic);
                    m.setTitle(headline);
                    m.setContent(content);
                    m.setTitleLength(headline.length());
                    m.setContentLength(content.length());
                    // createTime to be set later from impression timestamp

                    metadataMap.put(newsId, m);
                } catch (Exception ex) {
                    // 单行解析出错，打印日志继续
                    System.err.println("解析第 " + lineNum + " 行时出错: " + ex.getMessage());
                }
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to load news metadata", e);
        }
    }

    public NewsMetadata get(String newsId) {
        return metadataMap.get(newsId);
    }
}

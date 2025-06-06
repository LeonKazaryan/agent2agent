import jade.core.Agent;
import jade.core.behaviours.CyclicBehaviour;
import jade.lang.acl.ACLMessage;

public class ReceiverAgent extends Agent {
    private java.util.ArrayList<Integer> numbers = new java.util.ArrayList<>();

    protected void setup() {
        System.out.println("Агент 2 (JADE) запущен");

        addBehaviour(new CyclicBehaviour(this) {
            public void action() {
                ACLMessage msg = receive();
                if (msg != null) {
                    String content = msg.getContent();
                    try {
                        int number = Integer.parseInt(content);
                        System.out.println("Агент 2 получил число: " + number);
                        numbers.add(number);

                        // Считаем среднее
                        double average = numbers.stream().mapToInt(Integer::intValue).average().orElse(0);
                        System.out.println("Среднее значение: " + average);

                        // Даём рекомендацию
                        String recommendation = average < 5 ? "побольше" : "поменьше";
                        ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
                        reply.addReceiver(msg.getSender());
                        reply.setContent(recommendation);
                        send(reply);
                        System.out.println("Агент 2 отправил рекомендацию: " + recommendation);
                    } catch (NumberFormatException e) {
                        System.out.println("Ошибка: получено некорректное число");
                    }
                } else {
                    block(); // Ждём следующее сообщение
                }
            }
        });
    }
}
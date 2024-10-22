import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Users, Swords, Trophy } from 'lucide-react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  uid: string;
  display_name: string;
  description: string;
  collections: {
    skills: Skill[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    bot: Player;
  };
  stats: {
    player_score: number;
    bot_score: number;
    rounds: number;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { currentButtonIds, emitButtonClick } = useCurrentButtons();
  const { availableInteractiveThingIds, emitThingClick } = useThingInteraction();

  const { player, bot } = props.data.entities;
  const { player_score, bot_score, rounds } = props.data.stats;

  return (
    <div className="cq:container cq:mx-auto cq:p-4 cq:flex cq:flex-col cq:h-full cq:justify-between">
      <Alert className="cq:mb-4">
        <AlertTitle>How to Play</AlertTitle>
        <AlertDescription>
          Choose a skill to play against the bot. Rock beats Scissors, Scissors beats Paper, and Paper beats Rock.
        </AlertDescription>
      </Alert>

      <div className="cq:flex cq:justify-between cq:mb-4">
        <Card className="cq:p-4 cq:w-[48%]">
          <h2 className="cq:text-xl cq:font-bold cq:mb-2 cq:flex cq:items-center">
            <Users className="cq:mr-2" /> {player?.display_name || "Player"}
          </h2>
          <div className="cq:grid cq:grid-cols-3 cq:gap-2">
            {player?.collections.skills.map((skill) => (
              <Button
                key={skill.uid}
                onClick={() => emitThingClick(skill.uid)}
                disabled={!availableInteractiveThingIds.includes(skill.uid)}
                className="cq:text-sm"
              >
                {skill.display_name}
              </Button>
            ))}
          </div>
        </Card>

        <Card className="cq:p-4 cq:w-[48%]">
          <h2 className="cq:text-xl cq:font-bold cq:mb-2 cq:flex cq:items-center">
            <Swords className="cq:mr-2" /> {bot?.display_name || "Bot"}
          </h2>
          <div className="cq:grid cq:grid-cols-3 cq:gap-2">
            {bot?.collections.skills.map((skill) => (
              <Button key={skill.uid} disabled className="cq:text-sm">
                {skill.display_name}
              </Button>
            ))}
          </div>
        </Card>
      </div>

      <Card className="cq:p-4 cq:mb-4">
        <h2 className="cq:text-xl cq:font-bold cq:mb-2 cq:flex cq:items-center">
          <Trophy className="cq:mr-2" /> Score
        </h2>
        <div className="cq:flex cq:justify-between">
          <p>Player: {player_score}</p>
          <p>Bot: {bot_score}</p>
          <p>Rounds: {rounds}</p>
        </div>
      </Card>

      <div className="cq:flex cq:justify-center cq:space-x-4">
        {currentButtonIds.includes('play-again') && (
          <Button onClick={() => emitButtonClick('play-again')}>Play Again</Button>
        )}
        {currentButtonIds.includes('quit') && (
          <Button onClick={() => emitButtonClick('quit')} variant="outline">Quit</Button>
        )}
      </div>
    </div>
  );
}

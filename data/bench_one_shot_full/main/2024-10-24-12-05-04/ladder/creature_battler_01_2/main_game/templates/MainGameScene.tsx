import { useState, useEffect } from 'react';
import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections?: {
    skills?: Skill[];
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Player {
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const [turnMessage, setTurnMessage] = useState("");

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;
  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  useEffect(() => {
    if (availableButtonSlugs.length > 0) {
      setTurnMessage("Your turn!");
    } else {
      setTurnMessage("");
    }
  }, [availableButtonSlugs]);

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={player?.uid || ""}
          playerName={player?.display_name || "Unknown Player"}
          imageUrl="/placeholder-player.jpg"
        />
        <div>Battle in Progress</div>
        <PlayerCard
          uid={opponent?.uid || ""}
          playerName={opponent?.display_name || "Unknown Opponent"}
          imageUrl="/placeholder-opponent.jpg"
        />
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <Sword className="mb-2" />
          <CreatureCard
            uid={playerCreature?.uid || ""}
            name={playerCreature?.display_name || "Unknown"}
            imageUrl={`/creatures/${playerCreature?.uid || 'default'}.jpg`}
            hp={playerCreature?.stats.hp || 0}
          />
        </div>
        <div className="flex flex-col items-center">
          <Shield className="mb-2" />
          <CreatureCard
            uid={opponentCreature?.uid || ""}
            name={opponentCreature?.display_name || "Unknown"}
            imageUrl={`/creatures/${opponentCreature?.uid || 'default'}.jpg`}
            hp={opponentCreature?.stats.hp || 0}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          <p>Battle in progress...</p>
          {turnMessage && <p>{turnMessage}</p>}
        </div>
        <div className="flex justify-center space-x-2">
          {playerCreature?.collections?.skills?.map((skill: Skill) => {
            const buttonSlug = `use-skill-${skill.uid}`;
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                onClick={() => availableButtonSlugs.includes(buttonSlug) && emitButtonClick(buttonSlug)}
                disabled={!availableButtonSlugs.includes(buttonSlug)}
              />
            );
          })}
          {availableButtonSlugs.includes("quit") && (
            <SkillButton
              uid="quit"
              skillName="Quit"
              description="Quit the battle"
              stats=""
              onClick={() => emitButtonClick("quit")}
            />
          )}
        </div>
      </div>
    </div>
  );
}

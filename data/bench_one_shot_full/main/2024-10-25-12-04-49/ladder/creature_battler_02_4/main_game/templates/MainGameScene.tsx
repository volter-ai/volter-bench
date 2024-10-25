import { useCurrentButtons } from "@/lib/useChoices.ts";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { Shield, Swords, Play, X } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  uid: string;
  display_name: string;
  description: string;
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  description: string;
  collections: {
    creatures: Creature[];
  };
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderButtons = () => {
    return (
      <div className="flex space-x-2">
        {availableButtonSlugs.includes("play-again") && (
          <Button onClick={() => emitButtonClick("play-again")}>
            <Play className="mr-2 h-4 w-4" /> Play Again
          </Button>
        )}
        {availableButtonSlugs.includes("quit") && (
          <Button onClick={() => emitButtonClick("quit")}>
            <X className="mr-2 h-4 w-4" /> Quit
          </Button>
        )}
      </div>
    );
  };

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <span>Player: {props.data.entities.player?.display_name}</span>
        <span>Opponent: {props.data.entities.opponent?.display_name}</span>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={props.data.entities.player_creature?.uid || ""}
            name={props.data.entities.player_creature?.display_name || ""}
            imageUrl="/placeholder-player-creature.png"
            hp={props.data.entities.player_creature?.stats.hp || 0}
            maxHp={props.data.entities.player_creature?.stats.max_hp || 0}
          />
          <div className="mt-2 flex items-center">
            <Shield className="mr-1" />
            <span>{props.data.entities.player_creature?.stats.defense}</span>
            <Swords className="ml-2 mr-1" />
            <span>{props.data.entities.player_creature?.stats.attack}</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={props.data.entities.opponent_creature?.uid || ""}
            name={props.data.entities.opponent_creature?.display_name || ""}
            imageUrl="/placeholder-opponent-creature.png"
            hp={props.data.entities.opponent_creature?.stats.hp || 0}
            maxHp={props.data.entities.opponent_creature?.stats.max_hp || 0}
          />
          <div className="mt-2 flex items-center">
            <Shield className="mr-1" />
            <span>{props.data.entities.opponent_creature?.stats.defense}</span>
            <Swords className="ml-2 mr-1" />
            <span>{props.data.entities.opponent_creature?.stats.attack}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="mb-4">
          {props.data.entities.player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
        {renderButtons()}
      </div>
    </div>
  );
}

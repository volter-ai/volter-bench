import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { ArrowLeftCircle, XCircle } from 'lucide-react'
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full aspect-video bg-gray-100 flex flex-col">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <Button
          onClick={() => emitButtonClick('return-to-main-menu')}
          disabled={!availableButtonSlugs.includes('return-to-main-menu')}
        >
          <ArrowLeftCircle className="mr-2" /> Return to Main Menu
        </Button>
        <h1 className="text-xl font-bold">Battle Arena</h1>
        <Button
          onClick={() => emitButtonClick('quit-game')}
          disabled={!availableButtonSlugs.includes('quit-game')}
        >
          <XCircle className="mr-2" /> Quit Game
        </Button>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={player.uid}
            playerName={player.display_name}
            imageUrl={`/images/players/${player.uid}.jpg`}
          />
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl={`/images/creatures/${player_creature.uid}.jpg`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={opponent.uid}
            playerName={opponent.display_name}
            imageUrl={`/images/players/${opponent.uid}.jpg`}
          />
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl={`/images/creatures/${opponent_creature.uid}.jpg`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <h2 className="text-lg font-semibold mb-2">Your Skills</h2>
        <div className="grid grid-cols-2 gap-2">
          {player_creature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              disabled={!enabledUIDs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

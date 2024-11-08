import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { PlayerCard } from "@/components/ui/custom/PlayerCard";
import { CreatureCard } from "@/components/ui/custom/CreatureCard";
import { SkillButton } from "@/components/ui/custom/SkillButton";

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
    attack: number
    defense: number
    speed: number
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, opponent, player_creature, opponent_creature } = props.data.entities

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  return (
    <div className="h-screen w-screen flex items-center justify-center bg-slate-900">
      <div className="aspect-video w-full max-w-7xl h-auto flex flex-col">
        {/* HUD */}
        <nav className="h-[10%] bg-slate-800 flex justify-between items-center px-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/creatures/${player.uid}.png`}
          />
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/creatures/${opponent.uid}.png`}
          />
        </nav>

        {/* Battlefield */}
        <main className="h-[60%] flex justify-between items-center px-16 bg-slate-700">
          <div className="flex flex-col items-center gap-4">
            <div className="flex items-center gap-2">
              <Sword className="w-4 h-4" />
              <span>{player_creature.stats.attack}</span>
              <Shield className="w-4 h-4" />
              <span>{player_creature.stats.defense}</span>
              <Zap className="w-4 h-4" />
              <span>{player_creature.stats.speed}</span>
            </div>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/creatures/${player_creature.uid}.png`}
            />
          </div>

          <div className="flex flex-col items-center gap-4">
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl={`/creatures/${opponent_creature.uid}.png`}
            />
            <div className="flex items-center gap-2">
              <Sword className="w-4 h-4" />
              <span>{opponent_creature.stats.attack}</span>
              <Shield className="w-4 h-4" />
              <span>{opponent_creature.stats.defense}</span>
              <Zap className="w-4 h-4" />
              <span>{opponent_creature.stats.speed}</span>
            </div>
          </div>
        </main>

        {/* Controls */}
        <footer className="h-[30%] bg-slate-800 p-4">
          <div className="grid grid-cols-2 gap-4">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                disabled={!availableButtonSlugs.includes(skill.uid)}
                onClick={() => handleSkillClick(skill.uid)}
              />
            ))}
          </div>
        </footer>
      </div>
    </div>
  )
}

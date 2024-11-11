import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

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
    sp_attack: number
    sp_defense: number
    speed: number
  }
  meta: {
    prototype_id: string
    creature_type: string
  }
}

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
  meta: {
    skill_type: string
    is_physical: boolean
  }
}

interface GameUIData {
  entities: {
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const opponentCreature = props.data.entities.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div className="w-screen h-screen flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="w-screen h-screen flex flex-col">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 bg-gradient-to-b from-sky-100 to-sky-50">
        {/* Opponent Status */}
        <div className="flex items-center justify-center p-4">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl=""
            className="scale-75"
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={`${opponentCreature.uid}-battle`}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl=""
            className="scale-100"
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={`${playerCreature.uid}-battle`}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl=""
            className="scale-100"
          />
        </div>

        {/* Player Status */}
        <div className="flex items-center justify-center p-4">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl=""
            className="scale-75"
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-white p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {playerCreature.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              variant="outline"
              className="h-full text-lg"
            >
              <div className="flex flex-col items-center gap-2">
                {skill.meta.is_physical ? (
                  <Sword className="w-6 h-6" />
                ) : (
                  <Shield className="w-6 h-6" />
                )}
                {skill.display_name}
              </div>
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  )
}

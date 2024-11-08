import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, ArrowLeft } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"

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
  }
  meta: {
    image_front?: string
    image_back?: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  uid: string
  entities: {
    player: Player
    opponent: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities?.active_creature
  const opponentCreature = props.data.entities.opponent?.entities?.active_creature

  const handleSkillClick = () => {
    emitButtonClick('attack')
  }

  return (
    <div id={`${props.data.uid}-container`} className="h-screen w-screen aspect-video bg-slate-900 flex flex-col">
      {/* Battlefield Area */}
      <div id={`${props.data.uid}-battlefield`} className="h-2/3 grid grid-cols-2 gap-4 p-4 bg-slate-800">
        {/* Opponent Status */}
        <div id={`${props.data.uid}-opponent-status`} className="flex justify-start items-start">
          {opponentCreature && opponentCreature.__type === "Creature" && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={opponentCreature.meta.image_front || '/placeholder.png'}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div id={`${props.data.uid}-opponent-creature`} className="flex justify-end items-start">
          {opponentCreature && opponentCreature.__type === "Creature" && (
            <div className="w-48 h-48 flex items-center justify-center">
              <img 
                src={opponentCreature.meta.image_front || '/placeholder.png'} 
                alt={opponentCreature.display_name}
                className="max-w-full max-h-full object-contain"
              />
            </div>
          )}
        </div>

        {/* Player Creature */}
        <div id={`${props.data.uid}-player-creature`} className="flex justify-start items-end">
          {playerCreature && playerCreature.__type === "Creature" && (
            <div className="w-48 h-48 flex items-center justify-center">
              <img 
                src={playerCreature.meta.image_back || '/placeholder.png'} 
                alt={playerCreature.display_name}
                className="max-w-full max-h-full object-contain"
              />
            </div>
          )}
        </div>

        {/* Player Status */}
        <div id={`${props.data.uid}-player-status`} className="flex justify-end items-end">
          {playerCreature && playerCreature.__type === "Creature" && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={playerCreature.meta.image_back || '/placeholder.png'}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div id={`${props.data.uid}-ui`} className="h-1/3 bg-slate-700 p-4">
        <div id={`${props.data.uid}-actions`} className="grid grid-cols-2 gap-4">
          {/* Combat Actions */}
          <div id={`${props.data.uid}-skills`} className="space-y-2">
            {availableButtonSlugs.includes('attack') && 
             playerCreature?.__type === "Creature" && 
             playerCreature.collections.skills.map((skill) => (
              skill.__type === "Skill" && (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  description={skill.description}
                  stats={{
                    damage: skill.stats.base_damage,
                    type: skill.meta.skill_type
                  }}
                  onClick={handleSkillClick}
                >
                  {skill.display_name}
                </SkillButton>
              )
            ))}
          </div>

          {/* Other Actions */}
          <div id={`${props.data.uid}-other-actions`} className="space-y-2">
            {availableButtonSlugs.includes('swap') && (
              <Button 
                id={`${props.data.uid}-swap-button`}
                className="w-full" 
                onClick={() => emitButtonClick('swap')}
              >
                <Shield className="mr-2" /> Swap Creature
              </Button>
            )}
            {availableButtonSlugs.includes('back') && (
              <Button 
                id={`${props.data.uid}-back-button`}
                className="w-full" 
                onClick={() => emitButtonClick('back')}
              >
                <ArrowLeft className="mr-2" /> Back
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

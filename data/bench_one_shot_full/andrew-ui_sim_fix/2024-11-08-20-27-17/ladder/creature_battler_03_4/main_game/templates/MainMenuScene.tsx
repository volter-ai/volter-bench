import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, XCircle} from 'lucide-react'

interface BaseEntity {
    uid: string
    display_name: string
    description: string
    stats: Record<string, number>
    meta: Record<string, string>
    entities: Record<string, unknown>
    collections: Record<string, unknown>
    __type: string
}

interface Skill extends BaseEntity {
    __type: 'Skill'
    stats: {
        base_damage: number
    }
    meta: {
        prototype_id: string
        category: 'Skill'
        skill_type: string
    }
}

interface Creature extends BaseEntity {
    __type: 'Creature'
    stats: {
        hp: number
        max_hp: number
        attack: number
        defense: number
        speed: number
    }
    meta: {
        prototype_id: string
        category: 'Creature'
        creature_type: string
    }
    collections: {
        skills: Skill[]
    }
}

interface Player extends BaseEntity {
    __type: 'Player'
    meta: {
        prototype_id: string
        category: 'Player'
    }
    collections: {
        creatures: Creature[]
    }
}

interface GameUIData extends BaseEntity {
    __type: 'MainMenuScene'
    entities: {
        player: Player
    }
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    const buttonConfig = {
        play: { icon: Play, label: 'Play Game' },
        quit: { icon: XCircle, label: 'Quit Game' }
    }

    return (
        <div className="w-full h-full flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800 relative">
            <div className="absolute inset-0 bg-black/20" /> {/* Overlay for depth */}
            
            <div className="flex-1 flex items-center justify-center relative z-10">
                <h1 className="text-6xl font-bold text-white tracking-wider uppercase">
                    {props.data?.display_name || 'Game Title'}
                </h1>
            </div>

            <div className="flex flex-col gap-4 mb-16 relative z-10 w-full max-w-md">
                {availableButtonSlugs?.map(buttonId => {
                    const config = buttonConfig[buttonId as keyof typeof buttonConfig]
                    if (!config) return null

                    const Icon = config.icon

                    return (
                        <button
                            key={buttonId}
                            onClick={() => emitButtonClick(buttonId)}
                            className="flex items-center gap-3 px-8 py-4 bg-slate-700/90 hover:bg-slate-600/90 
                                     text-white rounded-lg transition-all duration-200
                                     justify-center group hover:scale-105"
                        >
                            <Icon 
                                size={24} 
                                className="group-hover:animate-pulse"
                            />
                            <span className="text-xl font-medium">
                                {config.label}
                            </span>
                        </button>
                    )
                })}
            </div>
        </div>
    )
}

import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  imageUrl: string
}

interface CreatureSubComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CreatureCardBase = Card
let CreatureCardHeaderBase = CardHeader
let CreatureCardContentBase = CardContent
let CreatureCardTitleBase = CardTitle

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, imageUrl, ...props }, ref) => {
    return (
      <CreatureCardBase uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CreatureCardHeaderBase uid={`${uid}-header`}>
          <CreatureCardTitleBase uid={`${uid}-title`}>{name}</CreatureCardTitleBase>
        </CreatureCardHeaderBase>
        <CreatureCardContentBase uid={`${uid}-content`} className="flex flex-col gap-4">
          <img 
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-cover rounded-md"
          />
          <div className="flex justify-between items-center">
            <span className="font-bold">HP:</span>
            <span>{hp}</span>
          </div>
        </CreatureCardContentBase>
      </CreatureCardBase>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCardBase = withClickable(CreatureCardBase)
CreatureCardHeaderBase = withClickable(CreatureCardHeaderBase)
CreatureCardContentBase = withClickable(CreatureCardContentBase)
CreatureCardTitleBase = withClickable(CreatureCardTitleBase)

export { CreatureCard }

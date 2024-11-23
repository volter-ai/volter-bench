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

interface SubComponentProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CreatureCardBase = Card
let CreatureCardHeaderBase = CardHeader
let CreatureCardContentBase = CardContent
let CreatureCardTitleBase = CardTitle

let CreatureCardHeader = React.forwardRef<HTMLDivElement, SubComponentProps>(
  ({ uid, ...props }, ref) => <CreatureCardHeaderBase uid={uid} ref={ref} {...props} />
)

let CreatureCardContent = React.forwardRef<HTMLDivElement, SubComponentProps>(
  ({ uid, ...props }, ref) => <CreatureCardContentBase uid={uid} ref={ref} {...props} />
)

let CreatureCardTitle = React.forwardRef<HTMLParagraphElement, SubComponentProps>(
  ({ uid, ...props }, ref) => <CreatureCardTitleBase uid={uid} ref={ref} {...props} />
)

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, imageUrl, ...props }, ref) => {
    return (
      <CreatureCardBase uid={uid} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CreatureCardHeader uid={`${uid}-header`}>
          <CreatureCardTitle uid={`${uid}-title`}>{name}</CreatureCardTitle>
        </CreatureCardHeader>
        <CreatureCardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-[200px] object-cover rounded-md"
            />
            <div className="flex justify-between items-center">
              <span className="font-bold">HP:</span>
              <span>{hp}</span>
            </div>
          </div>
        </CreatureCardContent>
      </CreatureCardBase>
    )
  }
)

CreatureCard.displayName = "CreatureCard"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardContent.displayName = "CreatureCardContent"
CreatureCardTitle.displayName = "CreatureCardTitle"

CreatureCard = withClickable(CreatureCard)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardContent = withClickable(CreatureCardContent)
CreatureCardTitle = withClickable(CreatureCardTitle)

export { CreatureCard }

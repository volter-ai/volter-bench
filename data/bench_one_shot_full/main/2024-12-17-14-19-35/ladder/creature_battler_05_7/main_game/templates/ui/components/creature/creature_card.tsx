import * as React from "react"
import { cn } from "@/lib/utils"
import withClickable from "@/lib/withClickable"
import { Card as ShadcnCard, CardContent as ShadcnCardContent, CardHeader as ShadcnCardHeader, CardTitle as ShadcnCardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface BaseCreatureProps {
  uid: string
}

let CreatureCardHeader = React.forwardRef<
  HTMLDivElement, 
  React.HTMLAttributes<HTMLDivElement> & BaseCreatureProps
>(({ className, uid, ...props }, ref) => (
  <ShadcnCardHeader ref={ref} className={className} {...props} />
))

let CreatureCardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement> & BaseCreatureProps
>(({ className, uid, ...props }, ref) => (
  <ShadcnCardTitle ref={ref} className={className} {...props} />
))

let CreatureCardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & BaseCreatureProps
>(({ className, uid, ...props }, ref) => (
  <ShadcnCardContent ref={ref} className={className} {...props} />
))

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement>, BaseCreatureProps {
  name: string
  image: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, image, currentHp, maxHp, ...props }, ref) => {
    return (
      <ShadcnCard ref={ref} className={cn("w-[350px]", className)} {...props}>
        <CreatureCardHeader uid={uid}>
          <CreatureCardTitle uid={uid}>{name}</CreatureCardTitle>
        </CreatureCardHeader>
        <CreatureCardContent uid={uid}>
          <div className="flex flex-col gap-4">
            <img
              src={image}
              alt={name}
              className="h-[200px] w-full object-contain"
            />
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>HP</span>
                <span>{`${currentHp}/${maxHp}`}</span>
              </div>
              <Progress value={(currentHp / maxHp) * 100} />
            </div>
          </div>
        </CreatureCardContent>
      </ShadcnCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"
CreatureCardHeader.displayName = "CreatureCardHeader"
CreatureCardTitle.displayName = "CreatureCardTitle"
CreatureCardContent.displayName = "CreatureCardContent"

CreatureCard = withClickable(CreatureCard)
CreatureCardHeader = withClickable(CreatureCardHeader)
CreatureCardTitle = withClickable(CreatureCardTitle)
CreatureCardContent = withClickable(CreatureCardContent)

export { CreatureCard, CreatureCardHeader, CreatureCardTitle, CreatureCardContent }
